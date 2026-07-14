const http = require('http');
// Removed global require for sync_obsidian to avoid cache issues

const PORT = 3123;

const server = http.createServer(async (req, res) => {
    // Add CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        res.writeHead(204);
        res.end();
        return;
    }

    if (req.method === 'POST' && req.url === '/api/sync') {
        try {
            // Delete cache so it always runs the latest version of sync_obsidian.js
            delete require.cache[require.resolve('./sync_obsidian')];
            const { syncObsidian } = require('./sync_obsidian');
            const result = await syncObsidian();
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify(result));
        } catch (error) {
            console.error(error);
            res.writeHead(500, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ success: false, error: error.message }));
        }
    } else {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('Not Found');
    }
});

server.listen(PORT, () => {
    console.log(`Sync Server running on http://localhost:${PORT}`);
    console.log('Keep this server running in the background to use the "갱신하기" button in the web UI.');
});
