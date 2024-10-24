from flask import Flask, jsonify, request

app = Flask(__name__)

# Data to be stored and retrieved
data = {
    "shortest_path_code": """
import java.util.Scanner;

class ShortestPath {
    int[][] graph; // Declare graph at the class level
    int V; // Number of vertices

    int minDistance(int dist[], boolean sptSet[]) {
        int min = Integer.MAX_VALUE, minIndex = -1;
        for (int v = 0; v < dist.length; v++) {
            if (!sptSet[v] && dist[v] < min) {
                min = dist[v];
                minIndex = v;
            }
        }
        return minIndex;
    }

    void printSolution(int dist[], int prev[], int src, int dest) {
        System.out.println("Shortest distance from vertex " + src + " to vertex " + dest + " is " + dist[dest]);
        System.out.print("Path: ");
        printPath(prev, dest);
        System.out.println();
    }

    void printPath(int prev[], int j) {
        if (prev[j] == -1) {
            System.out.print(j);
            return;
        }
        printPath(prev, prev[j]);
        System.out.print(" -> " + j);
    }

    void dijkstra(int src, int dest) {
        int dist[] = new int[V];
        boolean sptSet[] = new boolean[V];
        int prev[] = new int[V];

        for (int i = 0; i < V; i++) {
            dist[i] = Integer.MAX_VALUE;
            sptSet[i] = false;
            prev[i] = -1; // Initialize predecessors
        }

        dist[src] = 0;

        for (int count = 0; count < V - 1; count++) {
            int u = minDistance(dist, sptSet);
            sptSet[u] = true;

            for (int v = 0; v < V; v++) {
                if (!sptSet[v] && graph[u][v] != 0 && dist[u] != Integer.MAX_VALUE
                        && dist[u] + graph[u][v] < dist[v]) {
                    dist[v] = dist[u] + graph[u][v];
                    prev[v] = u; // Update predecessor
                }
            }
        }

        printSolution(dist, prev, src, dest);
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        ShortestPath sp = new ShortestPath();

        while (true) {
            System.out.println("Menu:");
            System.out.println("1. Enter graph (adjacency matrix)");
            System.out.println("2. Find shortest path using Dijkstra's algorithm");
            System.out.println("3. Exit");
            System.out.print("Choose an option: ");
            int choice = scanner.nextInt();

            switch (choice) {
                case 1:
                    System.out.print("Enter the number of vertices: ");
                    sp.V = scanner.nextInt(); // Set the number of vertices
                    sp.graph = new int[sp.V][sp.V]; // Initialize the graph

                    System.out.println("Enter the adjacency matrix (0 for no edge):");
                    for (int i = 0; i < sp.V; i++) {
                        for (int j = 0; j < sp.V; j++) {
                            sp.graph[i][j] = scanner.nextInt();
                        }
                    }
                    break;

                case 2:
                    System.out.print("Enter the source vertex (0 to " + (sp.V - 1) + "): ");
                    int src = scanner.nextInt();
                    System.out.print("Enter the destination vertex (0 to " + (sp.V - 1) + "): ");
                    int dest = scanner.nextInt();
                    sp.dijkstra(src, dest);
                    break;

                case 3:
                    System.out.println("Exiting...");
                    scanner.close();
                    return;

                default:
                    System.out.println("Invalid option. Please try again.");
            }
        }
    }
}

""",
    "crc_code": """
public class CRC {
   // Method to compute CRC remainder
   public static String computeCRC(String dataword, String divisor, int redundantBits) {
       // Append zeros to dataword
       String paddedDataword = appendZeros(dataword, redundantBits);
       // Perform CRC calculation
       String remainder = performDivision(paddedDataword, divisor);
       return remainder; // Remainder after division
   }

   // Method to manually append zeros to the dataword
   private static String appendZeros(String dataword, int numberOfZeros) {
       StringBuilder sb = new StringBuilder(dataword);
       for (int i = 0; i < numberOfZeros; i++) {
           sb.append('0');
       }
       return sb.toString();
   }

   // Method to perform binary division using XOR operations
   private static String performDivision(String data, String divisor) {
       int dataLength = data.length();
       int divisorLength = divisor.length();
       StringBuilder dividend = new StringBuilder(data);

       // Perform the division
       for (int i = 0; i <= dataLength - divisorLength; i++) {
           if (dividend.charAt(i) == '1') { // Only if the bit is 1
               for (int j = 0; j < divisorLength; j++) {
                   // XOR operation
                   char newChar = (dividend.charAt(i + j) == divisor.charAt(j)) ? '0' : '1';
                    dividend.setCharAt(i + j, newChar);
                 }
           }
       }
       // Extract the remainder
       return dividend.substring(dataLength - divisorLength + 1);
   }

   public static void main(String[] args) {
       // Predefined input values
       String dataword = "1011001"; // Example dataword
       String divisor = "1101";     // Example divisor
       int redundantBits = divisor.length() - 1; // Number of redundant bits

       // Sender Side
       System.out.println("Sender Side:");
       // Compute CRC remainder
       String paddedDataword = appendZeros(dataword, redundantBits);
       String remainder = computeCRC(dataword, divisor, redundantBits);
       // Compute codeword by appending the remainder to the dataword
       String codeword = dataword + remainder;
       // Output results
       System.out.println("Dataword: " + dataword);
       System.out.println("Divisor: " + divisor);
       System.out.println("Number of Redundant Bits: " + redundantBits);
       System.out.println("Padded Dataword: " + paddedDataword);
       System.out.println("Remainder: " + remainder);
       System.out.println("Codeword: " + codeword);

       // Simulate receiver side
       System.out.println("\\nReceiver Side:");
       // For demonstration, use the sent codeword as received data
       verifyData(codeword, divisor);
   }

   // Method to verify received data and calculate remainder
   public static void verifyData(String receivedCodeword, String divisor) {
       String calculatedRemainder = performDivision(receivedCodeword, divisor);
       System.out.println("Received Codeword: " + receivedCodeword);
       System.out.println("Calculated Remainder: " + calculatedRemainder);

       // Check if remainder is all zeros
       if (calculatedRemainder.equals("0".repeat(divisor.length() - 1))) {
           System.out.println("Data is intact, checksum matches.");
       } else {
           System.out.println("Data is corrupted, checksum does not match.");
       }
   }
}
""",
    "server_client_code": """
MyServer:
import java.io.*;
import java.net.*;

public class MyServer {
    public static void main(String[] args) {
        try {
            ServerSocket ss = new ServerSocket(6666);
            System.out.println("Server is waiting for a client...");

            Socket s = ss.accept();
            System.out.println("Client connected.");

            DataInputStream dis = new DataInputStream(s.getInputStream());
            String str = dis.readUTF();
            System.out.println("Message from client: " + str);

            dis.close();
            s.close();
            ss.close();
        } catch (Exception e) {
            System.out.println("Error: " + e);
        }
    }
}

MyClient:
import java.io.*;
import java.net.*;

public class MyClient {
    public static void main(String[] args) {
        try {
            Socket s = new Socket("localhost", 6666);
            System.out.println("Connected to the server.");

            DataOutputStream dout = new DataOutputStream(s.getOutputStream());
            dout.writeUTF("Hello Server");
            dout.flush();

            dout.close();
            s.close();
        } catch (Exception e) {
            System.out.println("Error: " + e);
        }
    }
}
""",
    "crc_function": """
# Function to perform XOR between two binary strings
def xor(a, b):
    result = ""
    for i in range(len(b)):
        result += str(int(a[i]) ^ int(b[i]))  # XOR each bit
    return result

# Function to calculate CRC remainder
def calculate_crc(data, divisor):
    # Append zeros to the data (same length as the divisor minus 1)
    appended_data = data + "0" * (len(divisor) - 1)
    
    # Perform the division process
    current_bits = appended_data[:len(divisor)]

    # Continue until all bits are processed
    for i in range(len(divisor), len(appended_data) + 1):
        if current_bits[0] == '1':  # Perform XOR with divisor if the leading bit is 1
            current_bits = xor(current_bits, divisor)  # XOR the divisor
        else:  # Perform XOR with zeros if the leading bit is 0
            current_bits = xor(current_bits, '0' * len(divisor))

        if i < len(appended_data):
            current_bits += appended_data[i]  # Bring down the next bit

        current_bits = current_bits.lstrip('0')  # Remove leading zeros

        # If current_bits is empty, reset it to 0
        if current_bits == "":
            current_bits = '0' * len(divisor)

    # The remainder is the CRC code
    return current_bits

# Example usage
data = "1101011111"  # Binary data to send
divisor = "10011"    # Divisor (polynomial)

print(f"Data: {data}")
print(f"Divisor: {divisor}")

# Calculate and print the CRC remainder
calculated_crc = calculate_crc(data, divisor)
print(f"Calculated CRC: {calculated_crc}")
"""
}



@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
