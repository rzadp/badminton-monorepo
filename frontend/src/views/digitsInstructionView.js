import React, {Component} from 'react';
import Paper from '@material-ui/core/Paper';

export default class DigitsInstructionView extends Component {
  static propTypes = {

  };

  render() {
    return (
      <Paper style={{padding: '30px', margin: '70px', display: 'inline-block', width: '380px', float: 'left'}}>
        <p>Aplikacja wykorzystuje wytrenowaną sieć CNN z poniszego tutoriala do wykrywania cyfr.</p>
        <a href='https://js.tensorflow.org/tutorials/mnist.html'>Tutorial</a>
      </Paper>
    );
  }
}
