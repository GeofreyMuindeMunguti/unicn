import Link from 'next/link';
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

// form validation schema
const schema = z
  .object({
    reset_code: z.string().min(3, 'Must be at least 3 characters'),
    password: z.string().min(1, 'Enter your password'),
    confirm_password: z.string().min(1, 'Required field'),
  })
  .refine((data) => data.password === data.confirm_password, {
    message: "Passwords don't match",
    path: ['confirm_password'],
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

    const payload = {
      email: router.query.email as string,
      reset_code: formData.reset_code,
      password: formData.password,
    };
    const [err] = await to(axios.post('auth/password-reset/', payload));

    if (err) {
      const errMessage = apiError(err);
      toast.error(errMessage);
      setStatus('rejected');
      return;
    }

    setStatus('resolved');
    toast.success('Your password has been reset');
    router.push('/login');
  };

  return (
    <AuthLayout subtitle="Set New Password" title="Reset Password">
      <Form.Container onSubmit={handleSubmit(onSubmit)}>
        <Form.Field hasError={errors.password}>
          <label htmlFor="password">Password</label>
          <input
            type="password"
            placeholder="Enter new password"
            {...register('password')}
          />
        </Form.Field>
        <Form.Field hasError={errors.confirm_password}>
          <label htmlFor="confirm_password">Confirm Password</label>
          <input
            type="password"
            placeholder="Confirm new password"
            {...register('confirm_password')}
          />
        </Form.Field>
        <Form.Field hasError={errors.reset_code}>
          <label htmlFor="reset_code">Reset Code</label>
          <input
            type="password"
            placeholder="Enter reset code"
            {...register('reset_code')}
          />
        </Form.Field>
        <Form.Button>
          <Button disabled={disableBtn} loading={isLoading}>
            Reset Password
          </Button>
        </Form.Button>
        <Form.FooterCaption>
          <span>Already have login credentials?</span>{' '}
          <Link href="/login">
            <a>Sign in</a>
          </Link>
        </Form.FooterCaption>
      </Form.Container>
    </AuthLayout>
  );
};

export default ResetPasswordPage;
