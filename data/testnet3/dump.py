import subprocess
import json

SKIP_COINBASES = False

def get_block_hash(height):
    result = subprocess.run(['src/bitcoin-cli', 'getblockhash', str(height)], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Error getting block hash: {result.stderr.strip()}")
    return result.stdout.strip()

def get_block(block_hash):
    result = subprocess.run(['src/bitcoin-cli', 'getblock', block_hash, '2'], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Error getting block: {result.stderr.strip()}")
    return json.loads(result.stdout)

def main():
    output_file = 't3_txs.json'
    with open(output_file, 'w') as f:
        f.write("[")
        end = 547
        first = True
        for height in range(0, end):
            block_hash = get_block_hash(height)
            block_data = get_block(block_hash)
            txs = block_data['tx']
            if first:
                first = False
            else:
                f.write(",")
            json.dump(txs, f, indent=4)
            print(f"Block {height} done")

        f.write("]")

if __name__ == '__main__':
    main()
