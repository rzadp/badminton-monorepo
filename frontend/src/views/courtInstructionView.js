import React, {Component} from 'react';
import Paper from '@material-ui/core/Paper';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Divider from '@material-ui/core/Divider';

export default class CourtInstructionView extends Component {
  static propTypes = {

  };

  render() {
    return (
      <Paper style={{paddingTop: '60px', paddingBottom: '60px', width: '400px'}}>
        <Table style={{marginLeft: 'auto', marginRight: 'auto', width: 'auto'}}>
          <TableHead>
            <TableRow>
              <TableCell>Ruch</TableCell>
              <TableCell>Klawisz</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            <TableRow>
              <TableCell>Góra/dół</TableCell>
              <TableCell>Q/E</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>Przód/Tył/Lewo/Prawo</TableCell>
              <TableCell>WASD</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>Obrót kamery</TableCell>
              <TableCell>Myszka z lewym</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>Ruch ludzików</TableCell>
              <TableCell>R</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>Anotacje</TableCell>
              <TableCell>N</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>Zapisz obraz</TableCell>
              <TableCell>J</TableCell>
            </TableRow>
          </TableBody>
        </Table>
        <Table style={{marginTop: '40px', marginLeft: 'auto', marginRight: 'auto', width: 'auto'}}>
          <TableHead>
            <TableRow>
              <TableCell>Oś układu</TableCell>
              <TableCell>Kolor</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            <TableRow>
              <TableCell>Oś X</TableCell>
              <TableCell>Czerwony</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>Oś Y</TableCell>
              <TableCell>Zielony</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>Oś Z</TableCell>
              <TableCell>Niebieski</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </Paper>
    );
  }
}
