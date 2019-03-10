import React from "react";
import VehicleCard from "./VehicleCard";

class Vehicles extends React.Component {
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
      <table>
        <tbody>
          <tr>
            {this.props.vehicles.map((car, key) => (
              <td key={key}>
                {console.log(car)}
                <VehicleCard car={car} />
              </td>
            ))}            
          </tr>
        </tbody>
      </table>
    );
  }
}

export default Vehicles;
