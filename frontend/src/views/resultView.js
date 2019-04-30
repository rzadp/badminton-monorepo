import React, {Component} from 'react';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import PropTypes from 'prop-types';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import RefreshIcon from '@material-ui/icons/Refresh';
import Paper from '@material-ui/core/Paper';

export default class ResultView extends Component {
  static propTypes = {
    result: PropTypes.any
  };

  render() {
    const displayedResult = Number.isInteger(this.props.result) ? this.props.result : '-';

    return (
      <Paper style={{padding: '30px', margin: '70px', display: 'inline-block', width: '280px', float: 'right'}}>
        <p>Result:</p>
        <div style={{fontSize: '32px'}}>
          <p >{displayedResult}</p>
        </div>
      </Paper>
    );
  }
}
