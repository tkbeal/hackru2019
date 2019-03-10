import React, { Component } from "react";
import axios from "axios";
import Smartcar from "@smartcar/auth";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faUser, faKey } from "@fortawesome/fontawesome-free-solid";
import WithLoading from "./components/WithLoading";

import Connect from "./components/Connect";
import Vehicles from "./components/Vehicle";

const VehiclesWithLoading = WithLoading(Vehicles);

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      vehicles: {},
      logged_in: false,
      authorized: false,
      loading: false
    };

    this.authorize = this.authorize.bind(this);

    this.onComplete = this.onComplete.bind(this);

    // TODO: Authorization Step 1: Initialize the Smartcar object
    this.smartcar = new Smartcar({
      clientId: "e8236e6a-5e3d-4503-9b86-1e2181c6e4a8",
      redirectUri:
        "https://javascript-sdk.smartcar.com/redirect-2.0.0?app_origin=http://localhost:3000",
      scope: [
        "read_vehicle_info read_odometer read_location control_security control_security:lock read_vin"
      ],
      testMode: true,
      onComplete: this.onComplete //What should this do?
    });
  }

  onComplete(err, code, status) {
    // TODO: Authorization Step 3: Receive the authorization code
    this.setState({ loading: true, authorized: true });
    console.log("Set loading to true");

    return axios
      .get(`http://localhost:8000/exchange?code=${code}`)
      .then(() => {
        return axios.get(`http://localhost:8000/vehicle`);
      })
      .then(res => {
        console.log("got data");
        this.setState({ vehicles: res.data, loading: false });
      });
  }

  logIn = () => {
    console.log("logging in");
    this.setState({ logged_in: true });
  };

  authorize() {
    // TODO: Authorization Step 2a: Launch the authorization flow
    this.smartcar.openDialog({ forcePrompt: true });
  }

  render() {
    return this.state.logged_in ? (
      this.state.authorized ? (
        <div style={styles.garageContainer}>
          <h2>My Cars:</h2>
          <VehiclesWithLoading
            loading={this.state.loading}
            vehicles={this.state.vehicles}
          />
        </div>
      ) : (
        <Connect onClick={this.authorize} />
      )
    ) : (
      <div style={styles.wrapper}>
        <div style={styles.loginContainer}>
          <h2 style={{ marginTop: 40 }}>Sign-in</h2>
          <form action="" style={styles.form}>
            <div style={styles.loginRow}>
              <FontAwesomeIcon icon={faUser} size="2x" />
              <input
                type="text"
                placeholder=" Username"
                style={styles.loginInput}
              />
            </div>
            <div style={styles.loginRow}>
              <FontAwesomeIcon icon={faKey} size="2x" />
              <input
                type="password"
                placeholder=" Password"
                style={styles.loginInput}
              />
            </div>
          </form>
          <button
            type="button"
            onClick={() => this.logIn()}
            style={styles.loginButton}
          >
            Log In
          </button>
        </div>
      </div>
    );
  }
}

const styles = {
  wrapper: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    width: "100%",
    height: "100vh",
    backgroundColor: "rgb(250,250,250)"
  },
  loginContainer: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    backgroundColor: "white",
    width: 280,
    height: 275,
    boxShadow: "0px 1px 1px 1px rgba(0,0,0,0.4)",
    borderRadius: 8
  },
  form: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center"
  },
  loginRow: {
    display: "flex",
    alignItems: "center",
    marginBottom: 20,
    maxWidth: 400
  },
  loginInput: {
    borderRadius: 5,
    height: 30,
    marginLeft: 10,
    fontSize: "16px"
  },
  loginButton: {
    borderRadius: 5,
    fontSize: 18,
    padding: 5,
    paddingLeft: 20,
    paddingRight: 20,
    backgroundColor: "rgba(147, 255, 183, 0.4)",
    color: "dark-gray"
  },
  garageContainer: {
    width: '100%',
    height: '100vh',
  }
};

export default App;
