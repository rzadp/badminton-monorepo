import React, {Component} from 'react';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import PropTypes from 'prop-types';
import Button from '@material-ui/core/Button';

export default class AppBarView extends Component {
  static propTypes = {
    selectedPage: PropTypes.string,
    onPageSelected: PropTypes.func
  };

  render() {
    const buttonStyle = {marginRight: '20px'};
    return (
      <div>
        <AppBar position="static" color="primary">
          <Toolbar>
            <Typography variant="h6" color="inherit" style={{marginRight: '20px'}}>Badminton</Typography>
            <Button variant="contained" disabled={this.props.selectedPage === 'court'} color="primary" onClick={() => this.props.onPageSelected('court')} style={buttonStyle}>Court</Button>
            <Button variant="contained" disabled={this.props.selectedPage === 'digits'} color="primary" onClick={() => this.props.onPageSelected('digits')} style={buttonStyle}>Digits</Button>
            <span style={{flexGrow: 1}}/>
          </Toolbar>
        </AppBar>
      </div>
    );
  }
}
