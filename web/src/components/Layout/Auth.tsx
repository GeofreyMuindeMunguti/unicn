import React from 'react';
import styled from 'styled-components';

import Logo from '../Logo/Logo';

type Props = {
  children: React.ReactNode;
  title: string;
  subtitle: string;
};

const MainContainer = styled.section`
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  height: 100vh;
`;

const BackgroundImage = styled.div`
  background: url('/images/auth-background.png');
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
`;

const FormContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 0;

  & > * {
    width: 50rem;
  }
`;

const AppHeader = styled.div`
  margin: 8rem 0 5rem;
  text-transform: uppercase;
  border-bottom: 1px solid var(--color-dark-gray);

  h3 {
    color: var(--primary-color);
    font-size: 1.6rem;
    font-weight: 700;
  }

  p {
    font-weight: 500;
  }
`;

const AuthLayout: React.FC<Props> = (props) => {
  return (
    <MainContainer>
      <FormContainer>
        <div>
          <Logo />
          <AppHeader>
            <h3>{props.title}</h3>
            <p>{props.subtitle}</p>
          </AppHeader>
        </div>
        <div>{props.children}</div>
      </FormContainer>
      <BackgroundImage />
    </MainContainer>
  );
};

export default AuthLayout;
