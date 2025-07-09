import axios from 'axios';

function Logout() {

  const handleLogout = async (e) => {
    e.preventDefault();
    // Clear the access token from local storage
    try {
      const response = await axios.post(
        "http://localhost:8000/logout",
        {},
        {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          }
        }
      );
      console.log("Logout response:", response);
      if (response.status === 200) {
        console.log("Logout successful");
      } else {
        console.error("Logout failed");
      }
    } catch (error) {
      console.error("Error logging out:", error);
      alert("Failed to log out. Please try again.");
    }
    localStorage.removeItem('access_token');
    // Optionally, you can redirect to a login page or refresh the page
    window.location.reload();
  }

  return (
    <>
      <button onClick={handleLogout}>Logout</button>
    </>
  );
}

export default Logout;