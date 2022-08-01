import type { NextPage } from 'next';
import styled from 'styled-components';

const AlignCenter = styled.div`
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const HomePage: NextPage = () => {
  return (
    <AlignCenter>
      <h2>Here we go</h2>
    </AlignCenter>
  );
};

export default HomePage;
