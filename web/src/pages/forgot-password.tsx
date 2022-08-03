import Link from 'next/link';
import styled from 'styled-components';
import to from 'await-to-js';
import toast from 'react-hot-toast';
import type { NextPage } from 'next';
import { z } from 'zod';
import { useRouter } from 'next/router';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

import apiError from 'src/utils/api';
import useStatus from 'src/hooks/useStatus';
import { axios } from 'src/utils/axios';
import { formHasValidationErrors } from 'src/utils/helperFunctions';

import * as Form from 'src/components/Form/Form';
import AuthLayout from 'src/components/Layout/Auth';
import Button from 'src/components/Button/Button';

type FormValues = z.infer<typeof schema>;

const Caption = styled.p`
  margin-bottom: 5rem;
`;

// form validation schema
const schema = z.object({
  email: z.string().min(1, 'Required field').email("That's not a valid email"),
});

const ResetPasswordPage: NextPage = () => {
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
  const onSubmit = async (formData: FormValues) => {
    setStatus('pending');

    const [err] = await to(axios.post('auth/reset-code/', formData));

    if (err) {
      const errMessage = apiError(err);
      toast.error(errMessage);
      setStatus('rejected');
      return;
    }

    setStatus('resolved');
    toast.success("We've sent you an email with a reset code");
    router.push(`/reset-password?email=${formData.email}`);
  };

  return (
    <AuthLayout subtitle="Don't worry" title="Forgot your password?">
      <Caption>
        Just enter your registered email address & we are going to send you a one
        time recovery code that you will need to enter in the next screen to reset
        your password.
      </Caption>
      <Form.Container onSubmit={handleSubmit(onSubmit)}>
        <Form.Field hasError={errors.email}>
          <label htmlFor="email">Email Address</label>
          <input
            type="email"
            placeholder="Enter your email address"
            {...register('email')}
          />
        </Form.Field>
        <Link href="/login">
          <a>Back to login</a>
        </Link>
        <Form.Button>
          <Button disabled={disableBtn} loading={isLoading}>
            Request password reset
          </Button>
        </Form.Button>
      </Form.Container>
    </AuthLayout>
  );
};

export default ResetPasswordPage;
