import * as fs from 'node:fs';
import * as path from 'node:path';
import * as crypto from 'node:crypto';

/**
 * Validates the generated image and copies it to the target output directory.
 */
function main() {
    const inputPath = path.join(process.cwd(), 'out', 'entry.png');
    const outputDir = path.join(process.cwd(), 'output');
    const outputPath = path.join(outputDir, 'entry.png');

    console.log(`Reading image from ${inputPath}...`);

    if (!fs.existsSync(inputPath)) {
        console.error(`[ERROR] Input image not found at: ${inputPath}`);
        console.error('Please run "python3 generate.py" first to create the entry image.');
        process.exit(1);
    }

    const buffer = fs.readFileSync(inputPath);
    const size = buffer.length;

    // 1. Validate size (under 1 MiB)
    const MAX_SIZE = 1024 * 1024;
    if (size > MAX_SIZE) {
        const sizeMiB = (size / (1024 * 1024)).toFixed(2);
        console.error(`[ERROR] Image size (${sizeMiB} MiB) exceeds the 1 MiB limit.`);
        process.exit(1);
    }

    // 2. Validate PNG magic bytes
    const pngMagic = Buffer.from([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]);
    if (!buffer.subarray(0, 8).equals(pngMagic)) {
        console.error('[ERROR] Invalid file format. Expected a PNG image.');
        process.exit(1);
    }

    // 3. Validate dimensions (1024x1024)
    if (buffer.length < 24) {
        console.error('[ERROR] Image file is too small to contain valid PNG headers.');
        process.exit(1);
    }
    const width = buffer.readUInt32BE(16);
    const height = buffer.readUInt32BE(20);

    if (width !== 1024 || height !== 1024) {
        console.error(`[ERROR] Invalid dimensions: ${width}x${height}. Expected exactly 1024x1024 pixels.`);
        process.exit(1);
    }

    // Ensure output directory exists
    try {
        if (!fs.existsSync(outputDir)) {
            fs.mkdirSync(outputDir, { recursive: true });
        }
    } catch (err) {
        console.error(`[ERROR] Failed to create output directory: ${err.message}`);
        process.exit(1);
    }

    // Write bytes to output
    try {
        fs.writeFileSync(outputPath, buffer);
    } catch (err) {
        console.error(`[ERROR] Failed to write image to ${outputPath}: ${err.message}`);
        process.exit(1);
    }

    // Determinism check: sha256
    const hash = crypto.createHash('sha256').update(buffer).digest('hex');
    
    console.log('--- Submission Summary ---');
    console.log(`Status: VALID`);
    console.log(`Dimensions: ${width}x${height} px`);
    console.log(`File Size: ${size} bytes (${(size / 1024).toFixed(2)} KiB)`);
    console.log(`SHA256 Checksum: ${hash}`);
    console.log(`Output Location: ${outputPath}`);
    console.log('---------------------------');
}

main();
