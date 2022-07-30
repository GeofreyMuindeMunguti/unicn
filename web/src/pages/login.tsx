import Link from 'next/link';
import type { NextPage } from 'next';

import * as Form from 'src/components/Form/Form';
import AuthLayout from 'src/components/Layout/Auth';
import Button from 'src/components/Button/Button';

const LoginPage: NextPage = () => {
  return (
    <AuthLayout subtitle="Sign In" title="Welcome">
      <Form.Container>
        <Form.Field>
          <label htmlFor="email">Email</label>
          <input type="text" placeholder="Your email address" />
        </Form.Field>
        <Form.Field>
          <label htmlFor="password">Password</label>
          <input type="password" placeholder="Enter your password" />
        </Form.Field>
        <Link href="/forgot-password">
          <a>Forgot Password?</a>
        </Link>
        <Form.Button>
          <Button>Login</Button>
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
