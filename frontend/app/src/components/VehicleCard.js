import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCar, faLockOpen, faLock } from "@fortawesome/fontawesome-free-solid";

class VehicleCard extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      locked: true
    };
  }

  toggleLock = () => {
    this.setState({ locked: !this.state.locked });
  };

  render() {
    return (
      <div style={styles.card}>
        <FontAwesomeIcon icon={faCar} size="2x" />
        <div style={styles.firstRow}>
          <p>
            <b>Make: </b>
            {this.props.car.info.make}
          </p>
          <p>
            <b>Model: </b>
            {this.props.car.info.model}
          </p>
          <p>
            <b>Year: </b>
            {this.props.car.info.year}
          </p>
        </div>
        <div style={styles.secondRow}>
          {this.state.locked ? (
            <button style={styles.lockButton} onClick={() => this.toggleLock()}>
              <FontAwesomeIcon icon={faLock} />
              <h3> Locked</h3>
            </button>
          ) : (
            <button style={styles.lockButton} onClick={() => this.toggleLock()}>
              <FontAwesomeIcon icon={faLockOpen} />
              <h3> Unlocked</h3>
            </button>
          )}
        </div>
      </div>
    );
  }
}

const styles = {
  card: {
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
    width: 200,
    borderRadius: 10,
    backgroundColor: '#d34521',
    boxShadow: "0px 1px 1px 1px rgba(0,0,0,0.4)",
    paddingTop: 10,
    paddingBottom: 10,
    color: 'white',
  },
  firstRow: {
    display: "flex",
    flexDirection: "column",
    justifyContent: "space-evenly"
  },
  secondRow: {
    display: "flex",
    justifyContent: "space-evenly"
  },
  lockButton: {
    backgroundColor: 'rgb(255, 124, 91)',
    display: 'flex',
    justifyContent: 'space-evenly',
    alignItems: 'center',
    borderRadius: 5,
    border: 'none', 
    minWidth: 125
  }
};

export default VehicleCard;
