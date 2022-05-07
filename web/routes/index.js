var express = require('express');
var router = express.Router();
const mysql = require('mysql');

const connection = mysql.createConnection({
	host: '***REMOVED***',
	user: 'piano',
	password: 'fundamental',
	database: 'pianotuning'
})

/* GET home page. */
router.get('/', function(req, res, next) {
	connection.connect()
	connection.query('select * from pianos', (err, rows, fields) => {
		res.render('index', { title: 'Express', data: JSON.stringify(rows) });
	})
	connection.end()
});

module.exports = router;
