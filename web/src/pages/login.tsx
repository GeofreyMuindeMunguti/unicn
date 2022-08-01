import Link from 'next/link';
import toast from 'react-hot-toast';
import type { NextPage } from 'next';
import { z } from 'zod';
import { useRouter } from 'next/router';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { signIn, SignInResponse } from 'next-auth/react';

import useStatus from 'src/hooks/useStatus';
import { formHasValidationErrors } from 'src/utils/helperFunctions';

import * as Form from 'src/components/Form/Form';
import AuthLayout from 'src/components/Layout/Auth';
import Button from 'src/components/Button/Button';

type FormValues = z.infer<typeof schema>;

// form validation schema
const schema = z.object({
  email: z.string().min(1, 'Required field').email("That's not a valid email"),
  password: z.string().min(1, 'Enter your password'),
});

const LoginPage: NextPage = () => {
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

    const res = await signIn('signin', {
      ...data,
      redirect: false,
      callbackUrl: `${window.location.origin}/dashboard`,
    });

    if (res) {
      const apiResponse = res as SignInResponse;

      if (apiResponse.error) {
        setStatus('rejected');
        toast.error(apiResponse.error);
      } else if (apiResponse.url) {
        router.push(apiResponse.url);
      }
    }
  };

  return (
    <AuthLayout subtitle="Sign In" title="Welcome">
      <Form.Container onSubmit={handleSubmit(onSubmit)}>
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
        <Link href="/forgot-password">
          <a>Forgot Password?</a>
        </Link>
        <Form.Button>
          <Button disabled={disableBtn} loading={isLoading}>
            Login
          </Button>
        </Form.Button>
        <Form.FooterCaption>
          <span>Are you new here, please</span>{' '}
          <Link href="/">
            <a>contact</a>
          </Link>{' '}
          for setup
        </Form.FooterCaption>
      </Form.Container>
    </AuthLayout>
  );
};

export default LoginPage;
