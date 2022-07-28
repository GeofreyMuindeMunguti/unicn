import { createGlobalStyle } from 'styled-components';

// All global styles used across the dashboard are defined here. This includes
// css variables, css resets, and global typography styles.

const GlobalStyles = createGlobalStyle`
    /* css variables */
    :root {
     --primary-color: #093EF9;
     --primary-background-color: #ffffff;
     --text-color: #263238;
     --text-color-light: #ffffff;
     --error-color: #c72e2e;
     --color-green: #04C500;
     --color-gray: #838383;
     --color-dark-gray: #d9d9d9;
     --input-border: #e1e4e8;
     --input-background-color: #f3f4f6;

     --font-primary: -apple-system,BlinkMacSystemFont,"Segoe UI","Roboto","Oxygen","Ubuntu","Cantarell","Fira Sans","Droid Sans","Helvetica Neue",sans-serif;
     --font-sub-headings: var(--font-primary);
     --font-headings: var(--font-primary);
     --font-links: var(--font-primary);

     --primary-border: 2px solid #eceff1;

     --primary-box-shadow: rgba(0, 0, 0, 0.05) 0px 1px 2px 0px;
     --inputs-box-shadow: rgba(0, 0, 0, 0.05) 0px 0px 0px 1px;
    }

    *,
    *::before,
    *::after {
      margin: 0;
      padding: 0;
      box-sizing: inherit;
    }

    *:focus {
      outline: none;
    }

    html {
      box-sizing: border-box;
      font-size: 62.5%; /* 62.5% of 16px base font size is 10px, therefore 1rem = 10px */
    }

    body {
      background-color: var(--primary-background-color);
      color: var(--text-color);
      font-family: var(--font-primary);
      font-size: 1.5rem;
      font-weight: 400;
      line-height: 1.5;
      overflow-x: hidden;
      min-height: 100vh;
      position: relative;

      @media (prefers-reduced-motion: no-preference) {
        html {
          scroll-behavior: smooth;
        }
      }
    }

    h1,
    h2 {
      font-family: var(--font-headings);
      font-weight: 700;
    }

    h3,
    h4 {
      font-family: var(--font-sub-headings);
      font-weight: 500;
    }

    a {
      cursor: pointer;
      color: var(--primary-color);
      text-decoration: none;
      font-family: var(--font-links);
      font-weight: 500;
      font-size: 1.4rem;
    }

    ul {
      list-style: none;
    }
`;

export default GlobalStyles;
