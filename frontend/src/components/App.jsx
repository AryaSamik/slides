import SignupForm from './SignupForm';
import LoginForm from './LoginForm';
import Generator from './Generate';
import Logout from './Logout';

function App() {

  return (
    <>
      <h1>Welcome to the YouTube Slide Generator</h1>
      <p>Please log in to continue.</p>
      <LoginForm />
      <SignupForm />
      <Generator />
      <Logout />
    </>
  );
}

export default App;
