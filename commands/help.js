
module.exports = {

    name: 'help',
    description: 'banner relacionado con los comandos',

    async execute(client, message, args) {
        const banner = `👑 Fundador:
    📌 **Kills** 
━━━━━━━━━━━━━━━━━━━━━━━
⚜ **Descripción:**
└─ 🛠️ Herramienta para consultas **Kimera**.

⚜ **Comandos Disponibles:**
├ 📋 **/lg** - Registrar usuario
├ 🌐 **/s** - Solicitar URL de carta
├ 📜 **/d** - Solicitar PDF de carta
├ ⚡ **/r** - Solicitar RECIBO de luz 
└ 📷 **/i** - Solicitar carta por foto

⚜ **Ejemplo de Uso:**
├ ✏️ **/s** 1337535
├ ✏️ **/d** 1337535
└ ✏️ **/i** [file]

⚜ **Reportes o Sugerencias:**
└─ 💬 Ayúdame a mejorar el bot   
📱 Escríbeme al número **915985153**.
━━━━━━━━━━━━━━━━━━━━━━━
    `;

        message.reply(banner);
    }
};
