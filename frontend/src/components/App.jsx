import SignupForm from './SignupForm';
import LoginForm from './LoginForm';
import Generator from './Generate';

function App() {

  return (
    <>
      <h1>Welcome to the YouTube Slide Generator</h1>
      <p>Please log in to continue.</p>
      <LoginForm />
      <SignupForm />
      <Generator />
    </>
  );
}

export default App;
