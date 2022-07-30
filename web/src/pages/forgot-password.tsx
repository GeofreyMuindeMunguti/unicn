import Link from 'next/link';
import styled from 'styled-components';
import type { NextPage } from 'next';

import * as Form from 'src/components/Form/Form';
import AuthLayout from 'src/components/Layout/Auth';
import Button from 'src/components/Button/Button';

const Caption = styled.p`
  margin-bottom: 5rem;
`;

const ResetPasswordPage: NextPage = () => {
  return (
    <AuthLayout subtitle="Don't worry" title="Forgot your password?">
      <Caption>
        Just enter your registered email address & we are going to send you a one
        time recovery code that you will need to enter in the next screen to reset
        your password.
      </Caption>
      <Form.Container>
        <Form.Field>
          <label htmlFor="email">Email Address</label>
          <input type="email" placeholder="Enter your email address" />
        </Form.Field>
        <Link href="/login">
          <a>Back to login</a>
        </Link>
        <Form.Button>
          <Button>Request password reset</Button>
        </Form.Button>
      </Form.Container>
    </AuthLayout>
  );
};

export default ResetPasswordPage;
