
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLConnection;
import java.util.Map;
import java.util.Scanner;

import com.fasterxml.jackson.core.*;
import com.fasterxml.jackson.databind.*;
import com.fasterxml.jackson.annotation.*;

/**
 * Simple example of a robot communication interface to the (real or virtual)
 * robot over a network connection. It uses Java -> JSON -> HttpRequest ->
 * Network -> DssHost32 -> Lokarria(Robulab) -> MRDS4
 * 
 * Most methods can throw an exception - in this example, they are all thrown
 * out to the operating system. A real implementation should take care of the
 * different exception types.
 * 
 * This class needs the following Jackson JSON .jar files:
 * jackson-core-2.0.5.jar jackson-databind-2.0.5.jar
 * jackson-annotations-2.0.5.jar
 * 
 * Download them from http://wiki.fasterxml.com/JacksonDownload under Downloads,
 * 2.x.
 * 
 * @author Thomas Johansson, dept. of Computing Science, Umea University, Umea,
 *         Sweden Mail: thomasj@cs.umu.se
 */
public class RobotCommunication {
    private String host;
    private int port;
    private ObjectMapper mapper;

    /**
     * Create a new communications object. Normally the host is 'localhost' and
     * the port is 500000.
     * 
     * @param host
     * @param port
     */
    public RobotCommunication(String host, int port) {
	this.host = host;
	this.port = port;

	// This is used by the JSON library to convert to/from JSON
	mapper = new ObjectMapper();
    }

    /**
     * Send a request to the robot.
     * 
     * @param r
     *            request to send
     * @return response code from the connection (the web server)
     * @throws Exception
     */
    public int putRequest(Request r) throws Exception {
	URL url = new URL(host + ":" + port + r.getPath());

	HttpURLConnection connection = (HttpURLConnection) url.openConnection();
    
    connection.setConnectTimeout(1000); //set timeout to 1 second

	connection.setDoOutput(true);

	connection.setRequestMethod("POST");
	connection.setRequestProperty("Content-Type", "application/json");
	connection.setUseCaches(false);

	OutputStreamWriter out = new OutputStreamWriter(connection.getOutputStream());

	// construct a JSON string
	String json = mapper.writeValueAsString(r.getData());

	// write it to the web server
	out.write(json);
	out.close();

	// wait for response code
	int rc = connection.getResponseCode();

	return rc;
    }

    /**
     * Get a response from the robot
     * 
     * @param r
     *            response to fill in
     * @return response same as parameter
     * @throws Exception
     */
    public Response getResponse(Response r) throws Exception {
	URL url = new URL(host + ":" + port + r.getPath());
	System.out.println(url + " (this annoying message comes from RobotCommunication)");

	// open a connection to the web server and then get the resulting data
	URLConnection connection = url.openConnection();
	BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));

	// map it to a Java Map
	Map<String, Object> data = mapper.readValue(in, Map.class);
	r.setData(data);

	in.close();

	return r;
    }

    /**
     * Cast an object, that can be an Integer or a Double, to a double. This is
     * necessary since sometimes the JSON data from the robot is an Integer and
     * sometimes a Double
     * 
     * @param robotData
     *            Response Object    
     * @return response same as double
     */
    public static double convert2Double(Object robotData) {
	double robotData_double = 0.0;
	if (robotData instanceof Double)
	    robotData_double = (Double) robotData; // unboxing
	else if (robotData instanceof Integer) {
	    // System.out.println("Integer.....");
	    robotData_double = ((Integer) robotData).doubleValue(); // unboxing
	}
	return robotData_double;
    }

    // /**
    // * Send a request for an action to the robot. The request must be
    // correctly formatted JSON.
    // * The path is the actual path on the server where the request is sent.
    // * The string can be manually constructed or the ObjectMapper object can
    // be used.
    // * Look at the tutorial: http://wiki.fasterxml.com/JacksonInFiveMinutes,
    // * specifically the "Raw" Data Binding Example
    // *
    // * @param request
    // * @param path
    // * @return
    // * @throws Exception
    // */
    // public int putRequest(String request, String path) throws Exception
    // {
    // URL url = new URL(host + ":" + port + path);
    //
    // HttpURLConnection connection = (HttpURLConnection)url.openConnection();
    //
    // connection.setDoOutput(true);
    // connection.setRequestMethod("POST");
    // connection.setRequestProperty("Content-Type", "application/json");
    // connection.setUseCaches (false);
    //
    // OutputStreamWriter out = new OutputStreamWriter(
    // connection.getOutputStream());
    //
    // out.write(request);
    // out.close();
    //
    // int rc = connection.getResponseCode();
    //
    // return rc;
    // }
    //
    // /**
    // * Sends a response request to the robot, and returns a JSON string with
    // the result.
    // * The string can be decoded by decodeJson.
    // * The path is the actual path on the server where the request is sent.
    // *
    // * @param path
    // * @return
    // * @throws Exception
    // */
    // public String getResponse(String path) throws Exception
    // {
    // URL url = new URL(host + ":" + port + path);
    //
    // URLConnection connection = url.openConnection();
    // BufferedReader in = new BufferedReader(new InputStreamReader(
    // connection.getInputStream()));
    //
    // Scanner scanner = new Scanner(in);
    // String response = scanner.next();
    //
    // in.close();
    //
    // return response;
    // }
    //
    // /**
    // * Decode a JSON string to a Java Map. This Map object can contain further
    // Map objects.
    // *
    // * @param jsonString
    // * @return
    // * @throws JsonParseException
    // * @throws JsonMappingException
    // * @throws IOException
    // */
    // public Map<String, Object> decodeJson(String jsonString)
    // throws JsonParseException, JsonMappingException, IOException
    // {
    // return mapper.readValue(jsonString, Map.class);
    // }

}
