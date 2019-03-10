import React from "react";
import Loader from "react-loader-spinner";

function WithLoading(Component) {
  return function WithLoadingComponent({ loading, ...props }) {
    if (!loading) return <Component {...props} />;
    else {
      console.log("Loading component...");
      return (
        <div style={loadingStyle}>
          <h2>Loading Your Cars</h2> <Loader type="ThreeDots" height={80} width={80} />
        </div>
      );
    }
  };
}

const loadingStyle = {
  width: '100%', 
  height: '100vh', 
  display: 'flex', 
  flexDirection: 'column',
  justifyContent: 'center',
  alignItems: 'center',
}

export default WithLoading;
