import Head from "next/head";
import { Spinner, Stack, Container, Row, Card, Button } from "react-bootstrap";

const generateSummary = async () => {
  document.getElementById("spinner").classList.remove("d-none");
  const url = document.getElementById("input_url").value;
  const params = new URLSearchParams({ podcast_url: url });
  const res = await fetch(
    "http://ankushhome.duckdns.org:5001/summarize_podcast?" + params,
    {
      method: "GET",
    }
  );
  const data = await res.json();
  const summary = document.getElementById("summary");
  summary.innerHTML = data.summary;
  document.getElementById("spinner").classList.add("d-none");
};

export default function Home() {
  return (
    <Container className='container-lg'>
      <Head>
        <title>Summarizer App</title>
        <link rel='icon' href='/favicon-32x32.png' />
      </Head>
      <div className='d-flex flex-column mt-5 vh-100'>
        <div className='d-flex flex-column w-100 align-items-center'>
          <h1 className='text-center'>AI Podcast Summarizer</h1>
          <input
            className='form-control w-75 mt-3'
            type='text'
            placeholder='Enter Apple / Google Podcast URL'
            id='input_url'
          />
          <Button className='mt-3' onClick={generateSummary}>
            <Spinner
              className='d-none'
              as='span'
              size='sm'
              role='status'
              aria-hidden='true'
              id='spinner'
            />{" "}
            Summarize
          </Button>
        </div>
        <div className='mt-5' id='summary'></div>
      </div>
    </Container>
  );
}
