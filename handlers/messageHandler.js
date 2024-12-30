// whatsapp/handlers/messageHandlers.js

const Chance = require('chance');
const fs = require('fs');
const path = require('path');
const commands = require('../commands/index.js')
const download = require('../utils/download.js')
const solicitud = require('../utils/request.js');
const { measureMemory } = require('vm');

let statusp = false; // Estado inicial deshabilitado
const maxImages = 5; // Límite de imágenes
let imageCountp = 0;  // Contador de imágenes

module.exports = async (client, message) => {

    if (message.type === 'chat') {
        if (!message.body.startsWith('/') || message.body.length <= 1) return;

        const args = message.body.slice(1).trim().split(/ +/)
        const commandName = args.shift().toLowerCase()
        const command = commands.get(commandName)

        // console.log(command)

        await command.execute(client, message, args)

        if (args[0] === 'start') {

            imageCountp = command.getImageCount()
            // console.log(imageCountp)

            statusp = command.getStatus()
            // console.log(statusp)

        }

    }

    if (message.type === 'image') {
        if (!statusp) {
            message.reply('🚫 El procesamiento de imágenes está deshabilitado. Usa /f start para habilitarlo.');
            return;
        }

        const suministro = await download.mediaDownimage(message)

        // const jsonString = JSON.stringify(info);

        // Convertir la cadena JSON a bytes (UTF-8)
        // const bytes = new TextEncoder().encode(jsonString);

        const prediccion = await solicitud.localendpoint('prediccion',suministro.usuario)

        console.log(prediccion.suministro)

        // solicitud.popmensaje(prediccion, message)

        imageCountp++;

        // Comprueba si se alcanzó el límite
        if (imageCountp >= maxImages) {
            message.reply('⛔ iniciando resolucion formulario');
            statusp = false;

        }
    }
};
