import Head from "next/head";
import { Stack, Container, Row, Card, Button } from "react-bootstrap";

export default function Home() {
  return (
    <Container className='container-lg'>
      <Head>
        <title>Summarizer App</title>
        <link rel='icon' href='/favicon-32x32.png' />
      </Head>
      <div className='d-flex align-items-center vh-100'>
        <div className='d-flex flex-column w-100 align-items-center'>
          <h1 className='text-center'>AI Summarizer</h1>
          <input
            className='form-control w-75'
            type='text'
            placeholder='Enter URL'
          />
        </div>
      </div>
    </Container>
  );
}
