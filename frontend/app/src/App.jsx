import React, {Component} from 'react';
import axios from 'axios';
import Smartcar from '@smartcar/auth';

import Connect from './components/Connect';
import Vehicle from './components/Vehicle';

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      vehicle: {},
    };

    this.authorize = this.authorize.bind(this);

    this.onComplete = this.onComplete.bind(this);

    // TODO: Authorization Step 1: Initialize the Smartcar object
    this.smartcar = new Smartcar({
      clientId: 'e8236e6a-5e3d-4503-9b86-1e2181c6e4a8',
      redirectUri: 'https://javascript-sdk.smartcar.com/redirect-2.0.0?app_origin=http://localhost:3000',
      testMode: true,
      onComplete: this.onComplete,
    });
  }

  onComplete(err, code, status) {
    // TODO: Authorization Step 3: Receive the authorization code
    return axios.get(``);

    // TODO: Request Step 1: Obtain an access token

    // TODO: Request Step 2a: Get vehicle information
  }

  authorize() {
    // TODO: Authorization Step 2a: Launch the authorization flow
    this.smartcar.openDialog({forcePrompt: true});
  }

  render() {
    // TODO: Authorization Step 2b: Launch the authorization flow
    return(
      <Connect onClick={this.authorize}/>
    );

    // TODO: Request Step 2b: Get vehicle information
  }
}

export default App;
