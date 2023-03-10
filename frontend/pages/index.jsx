import Head from "next/head";
import { Button, Container, Spinner } from "react-bootstrap";

const generateSummary = async () => {
  const summary = document.getElementById("summary");
  summary.innerHTML = "";
  document.getElementById("spinner").classList.remove("d-none");
  const url = document.getElementById("input_url").value;
  const params = new URLSearchParams({ podcast_url: url });
  const res = await fetch(
    "https://gpt-summarizer.chatgpt.fun/summarize_podcast?" + params,
    {
      method: "GET",
    }
  );
  const data = await res.json();
  summary.innerHTML = `Podcast Title: ${data.podcast_title}\n${data.summary}`;
  document.getElementById("spinner").classList.add("d-none");
};

const populateInputURL = (element) => {
  element.preventDefault();
  document.getElementById("input_url").value =
    "https://podcasts.apple.com/us/podcast/healing-affirmations-for-the-soul/id1596171716?i=1000590025009";
};

export default function Home() {
  return (
    <Container className='container-lg'>
      <Head>
        <title>Summarizer App</title>
        <link rel='icon' href='/favicon-32x32.png' />
      </Head>
      <div
        className='border border-dark d-flex flex-column mt-5 p-5'
        style={{
          borderRadius: "15px",
        }}
      >
        <div className='d-flex flex-column w-100 align-items-center'>
          <h1 className='text-center'>AI Podcast Summarizer</h1>
          <p className='text-center w-75'>
            Enter the URL of an Apple or Google Podcast to get its summary using
            GPT-3.{" "}
            <a onClick={populateInputURL} href='#'>
              Click here
            </a>{" "}
            for an example. It can upto a couple of minutes to generate the
            summary depending on the length of the podcast.
          </p>
          <input
            className='form-control w-75 mt-1'
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
        <div
          className='mt-5'
          id='summary'
          style={{ whiteSpace: "pre-wrap" }}
        ></div>
      </div>
    </Container>
  );
}
