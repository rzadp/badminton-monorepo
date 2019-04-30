import React, {Component} from 'react';
import PropTypes from 'prop-types';
import CanvasView from 'views/canvasView';
import DigitsInstructionView from 'views/digitsInstructionView';
import ResultView from 'views/resultView';

export default class Digits extends Component {
  static propTypes = {
    services: PropTypes.object
  };

  constructor(props) {
    super(props);
    this.state = {
      result: ''
    };
  }

  componentDidMount() {

  }

  componentWillUnmount() {

  }

  render() {
    const handleClear = () => this.setState({result: null});

    const handlePredict = async(image) => {
      const result = this.props.services.model.predict(image);
      this.setState({result});
    };


    return (
      <div>
        <div className='content' style={{paddingTop: '60px', paddingBottom: '60px', margin: 'auto'}}>
          <DigitsInstructionView/>
          <CanvasView
            onPredict={handlePredict}
            onClear={handleClear}
          />
          <ResultView result={this.state.result}/>
        </div>
      </div>
    );
  }
}
