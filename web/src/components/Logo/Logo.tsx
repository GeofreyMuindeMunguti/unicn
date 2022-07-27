import React from 'react';
import styled from 'styled-components';

const Container = styled.div`
  display: flex;
  align-items: center;
`;

const Placeholder = styled.div`
  border-radius: 0.5rem;
  background-color: var(--color-dark-gray);
  display: grid;
  place-items: center;
  margin-right: 2rem;
  height: 10rem;
  width: 10rem;
`;

const LogoContent = styled.div`
  h2 {
    font-size: 1.8rem;
  }

  span {
    font-size: 1.4rem;
  }
`;

const Logo = () => {
  return (
    <Container>
      <Placeholder>Logo</Placeholder>
      <LogoContent>
        <h2>UNICN</h2>
        <span>Tagline</span>
      </LogoContent>
    </Container>
  );
};

export default Logo;
