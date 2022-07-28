import type { NextPage } from 'next';
import Image from 'next/image';
import styled from 'styled-components';

import Logo from 'src/components/Logo/Logo';
import Button from 'src/components/Button/Button';

const Section = styled.section`
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
`;

const Tagline = styled.p`
  margin: 4rem 0;

  span {
    color: var(--primary-color);
    text-transform: uppercase;
    font-weight: 700;
    font-size: 1.4rem;
  }
`;

const Subtitle = styled.h2`
  font-size: 1.6rem;
  margin-bottom: 2rem;
`;

const DownloadCards = styled.div`
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  column-gap: 2rem;
  margin: 3rem 0;
`;

const DownloadCard = styled.div<{ color?: string }>`
  border: 1px solid ${({ color }) => color ?? 'var(--primary-color)'};
  border-radius: 0.8rem;
  padding: 1.5rem 3rem;

  h3 {
    font-size: 1.4rem;
    font-weight: 700;
  }
`;

const Download = styled.div`
  display: grid;
  grid-template-columns: max-content 10rem;
  align-items: center;
  column-gap: 3rem;
  margin-top: 1rem;
`;

const DownloadIcon = styled.div`
  width: 4rem;
`;

const RedirectButton = styled.div`
  width: 20rem;
`;

const SuccessfulRegistration: NextPage = () => {
  return (
    <Section>
      <div>
        <Logo />
        <Tagline>
          You have successfully been registered on UNICN upon invite from{' '}
          <span>Company Name</span>
        </Tagline>
        <Subtitle>Download the app</Subtitle>
        <DownloadCards>
          <DownloadCard>
            <h3>Get it on app store</h3>
            <Download>
              <DownloadIcon>
                <Image
                  alt="app-store"
                  src="/icons/appstore.svg"
                  layout="responsive"
                  height={59}
                  width={58}
                />
              </DownloadIcon>
              <Button size="small">Get</Button>
            </Download>
          </DownloadCard>
          <DownloadCard color="var(--color-green)">
            <h3>Get it on playstore</h3>
            <Download>
              <DownloadIcon>
                <Image
                  alt="playstore"
                  src="/icons/playstore.svg"
                  layout="responsive"
                  height={52}
                  width={48}
                />
              </DownloadIcon>
              <Button color="var(--color-green)" size="small">
                Download
              </Button>
            </Download>
          </DownloadCard>
        </DownloadCards>
        <Subtitle>OR</Subtitle>
        <RedirectButton>
          <Button color="transparent">Process to dashboard</Button>
        </RedirectButton>
      </div>
    </Section>
  );
};

export default SuccessfulRegistration;
