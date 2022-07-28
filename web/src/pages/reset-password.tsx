import Link from 'next/link';
import type { NextPage } from 'next';

import * as Form from 'src/components/Form/Form';
import AuthLayout from 'src/components/Layout/Auth';
import Button from 'src/components/Button/Button';

const ResetPasswordPage: NextPage = () => {
  return (
    <AuthLayout subtitle="Set New Password" title="Reset Password">
      <Form.Container>
        <Form.Field>
          <label htmlFor="password">Password</label>
          <input type="password" placeholder="Enter new password" />
        </Form.Field>
        <Form.Field>
          <label htmlFor="confirm-password">Confirm Password</label>
          <input type="password" placeholder="Confirm new password" />
        </Form.Field>
        <Form.Field>
          <label htmlFor="code">Reset Code</label>
          <input type="code" placeholder="Enter reset code" />
        </Form.Field>
        <Link href="/reset-password">
          <a>Retry reset code?</a>
        </Link>
        <Form.Button>
          <Button>Reset Password</Button>
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
