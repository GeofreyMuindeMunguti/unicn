import type { NextPage } from 'next';
import Link from 'next/link';
import styled from 'styled-components';
import to from 'await-to-js';
import toast from 'react-hot-toast';
import { z } from 'zod';
import { useRouter } from 'next/router';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

import { axios } from 'src/utils/axios';
import apiError from 'src/utils/api';
import useStatus from 'src/hooks/useStatus';
import { formHasValidationErrors } from 'src/utils/helperFunctions';

import * as Form from 'src/components/Form/Form';
import Button from 'src/components/Button/Button';
import Logo from 'src/components/Logo/Logo';

type FormValues = z.infer<typeof schema>;

const Section = styled.section`
  display: grid;
  place-items: center;
  height: 100vh;
`;

const Container = styled.div`
  max-width: 65rem;
`;

const WelcomeText = styled.div`
  margin: 5rem 0 3rem;

  span {
    color: var(--primary-color);
    font-weight: 700;
    text-transform: uppercase;
  }
`;

const FormCaption = styled.p`
  color: var(--color-gray);
  font-size: 1.4rem;
  margin-bottom: 2rem;
`;

// form validation schema
const schema = z
  .object({
    email: z.string().min(1, 'Required field').email("That's not a valid email"),
    name: z.string().min(3, 'Must be at least 3 characters'),
    password: z.string().min(1, 'Enter your password'),
    confirm_password: z.string().min(1, 'Required field'),
  })
  .refine((data) => data.password === data.confirm_password, {
    message: "Passwords don't match",
    path: ['confirm_password'],
  });

const RegisterPage: NextPage = () => {
  const router = useRouter();
  const { setStatus, isLoading } = useStatus();
  const {
    formState: { errors },
    handleSubmit,
    register,
  } = useForm<FormValues>({
    resolver: zodResolver(schema),
  });
  const disableBtn = formHasValidationErrors(errors);

  // submit form
  const onSubmit = async (data: FormValues) => {
    setStatus('pending');

    const payload = {
      email: data.email,
      name: data.name,
      password: data.password,
      user_id: '37d16981-722e-45fc-9b9c-93d93f99ca29', // TODO: remove this hardcoded value
    };
    const [err] = await to(axios.post('auth/register', payload));

    if (err) {
      const errMessage = apiError(err);
      toast.error(errMessage);
      setStatus('rejected');
      return;
    }

    setStatus('resolved');
    router.push('/register/success');
  };

  return (
    <Section>
      <Container>
        <Logo />
        <WelcomeText>
          <p>
            <span>Company Name</span> is inviting you to the UNICN platform.
          </p>
        </WelcomeText>
        <FormCaption>Please fill in the form below to register.</FormCaption>
        <Form.Container onSubmit={handleSubmit(onSubmit)}>
          <Form.Grid>
            <Form.Field hasError={errors.name}>
              <label htmlFor="name">Username</label>
              <input type="text" placeholder="Your username" {...register('name')} />
            </Form.Field>
            <Form.Field hasError={errors.email}>
              <label htmlFor="email">Email</label>
              <input
                type="text"
                placeholder="Your email address"
                {...register('email')}
              />
            </Form.Field>
            <Form.Field hasError={errors.password}>
              <label htmlFor="password">Password</label>
              <input
                type="password"
                placeholder="Enter your password"
                {...register('password')}
              />
            </Form.Field>
            <Form.Field hasError={errors.confirm_password}>
              <label htmlFor="confirm_password">Confirm Password</label>
              <input
                type="password"
                placeholder="Confirm your password"
                {...register('confirm_password')}
              />
            </Form.Field>
          </Form.Grid>
          <Link href="/login">
            <a>Not ready!</a>
          </Link>
          <Form.Button>
            <Button disabled={disableBtn} loading={isLoading}>
              Register
            </Button>
          </Form.Button>
        </Form.Container>
      </Container>
    </Section>
  );
};

export default RegisterPage;
