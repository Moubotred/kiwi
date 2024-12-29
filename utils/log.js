function logMessage(message, type = 'info') {
    const timestamp = new Date().toISOString();
    
    switch (type) {
        case 'info':
            console.log(`[INFO] ${timestamp}: ${message}`);
            break;
        case 'warn':
            console.warn(`[WARN] ${timestamp}: ${message}`);
            break;
        case 'error':
            console.error(`[ERROR] ${timestamp}: ${message}`);
            break;
        default:
            console.log(`[INFO] ${timestamp}: ${message}`);
    }
}

function logMessageToFile(message, type = 'info') {
    const timestamp = new Date().toISOString();
    const logMessage = `[${type.toUpperCase()}] ${timestamp}: ${message}\n`;
    
    // Define la ruta del archivo donde guardar los mensajes de log
    const logFilePath = path.join(__dirname, 'logs.txt');
    
    // Escribe (o añade) el mensaje al archivo
    fs.appendFile(logFilePath, logMessage, (err) => {
        if (err) {
            console.error(`[ERROR] ${timestamp}: No se pudo escribir el log.`);
        }
    });
}

module.exports = {
    logMessageToFile,
};