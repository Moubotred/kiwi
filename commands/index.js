const fs = require('fs');
const path = require('path');

const commands = new Map();

// Leer todos los archivos dentro del directorio actual que terminen en `.js`
const commandFiles = fs.readdirSync(__dirname).filter(file => file.endsWith('.js') && file !== 'index.js');

for (const file of commandFiles) {
    const command = require(path.join(__dirname, file));
    commands.set(command.name, command);
}

module.exports = commands;
