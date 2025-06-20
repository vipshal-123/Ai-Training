import { useSelector } from "react-redux";

function Profile() {
  const selector = useSelector((user) => user.auth);

  return (
    <div className="profile-container">
      <h1>Welcome {selector.name}</h1>

      <div className="profile-info">
        <p>
          <strong>Email: {selector.email}</strong> 
        </p>
        <p>
          <strong>Google ID:</strong> 
        </p>
      </div>

    </div>
  );
}

export default Profile;
