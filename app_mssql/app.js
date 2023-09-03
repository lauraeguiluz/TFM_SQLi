const express = require('express');
const mssql = require('mssql');
const app = express();

const config = {
  user: 'admin',
  password: 'admin',
  server: 'localhost',
  database: 'Project',
  options: {
    encrypt: false, // Desactiva SSL
  },
};

async function fetchData(dni) {
  try {
    await mssql.connect(config);

    const query = `SELECT * FROM Estudiante WHERE dni = '${dni}'`;
    console.log("Query:", query);
    
    const output = await mssql.query(query);
    
    return output.recordset;
  } catch (error) {
    throw error;
  } finally {
    mssql.close();
  }
}

app.use(express.static(__dirname + '/static'));

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

app.get('/api/data', async (req, res) => {
  const dni = req.query.dni;

  try {
    const data = await fetchData(dni);
    res.json(data);
  } catch (error) {
    console.error('Error de base de datos:', error);
    res.status(500).send('Error de base de datos');
  }
});

app.listen(5000, '0.0.0.0', () => {
  console.log(`Servidor en ejecución en el puerto 5000`);
});
