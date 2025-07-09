import SignupForm from './SignupForm';
import LoginForm from './LoginForm';
import Generator from './Generate';
import Logout from './Logout';
import { useContext, useState } from 'react';
import { AuthContext } from '../contexts/AuthCountext';

function App() {
  const { authUser } = useContext(AuthContext);
  const [isnewuser, setisnewuser] = useState(false);
  return (
    <>
      <h1>Welcome to the YouTube Slide Generator</h1>
      {
        (!authUser)
        ?
        <>
          {(!isnewuser)?<LoginForm value={{isnewuser, setisnewuser}}/>:<></>}
          {(isnewuser)?<SignupForm value={{isnewuser, setisnewuser}}/>:<></>}
        </>
        :
        <></>
      }
      {(authUser)?<Generator />:<></>}
      {(authUser)?<Logout />:<></>}
    </>
  );
}

export default App;
