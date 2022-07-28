import type { NextPage } from 'next';
import Link from 'next/link';
import styled from 'styled-components';

import * as Form from 'src/components/Form/Form';
import Button from 'src/components/Button/Button';
import Logo from 'src/components/Logo/Logo';

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

const RegisterPage: NextPage = () => {
  return (
    <Section>
      <Container>
        <Logo />
        <WelcomeText>
          <p>
            <span>Company Name</span> is inviting you to the UNICN platform.
          </p>
        </WelcomeText>
        <FormCaption>
          Please fill in the form below to register.
        </FormCaption>
        <Form.Container>
          <Form.Grid>
            <Form.Field>
              <label htmlFor="name">Username</label>
              <input type="text" placeholder="Your username" />
            </Form.Field>
            <Form.Field>
              <label htmlFor="email">Email</label>
              <input type="text" placeholder="Your email address" />
            </Form.Field>
            <Form.Field>
              <label htmlFor="password">Password</label>
              <input type="password" placeholder="Enter your password" />
            </Form.Field>
            <Form.Field>
              <label htmlFor="confirm-password">Confirm Password</label>
              <input type="confirm-password" placeholder="Confirm your password" />
            </Form.Field>
          </Form.Grid>
          <Link href="/login">
            <a>Not ready!</a>
          </Link>
          <Form.Button>
            <Button>Register</Button>
          </Form.Button>
        </Form.Container>
      </Container>
    </Section>
  );
};

export default RegisterPage;
