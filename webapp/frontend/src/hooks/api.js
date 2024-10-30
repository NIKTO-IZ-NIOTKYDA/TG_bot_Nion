const __URL_API__ = 'http://localhost/api';

const AddNetSchool = async (UserID, Login, Password, Key) => {
    // Create the request body
    const requestBody = {
        UserID,
        Login,
        Password,
        Key
    };

    try {
        // Make the POST request
        const response = await fetch(`${__URL_API__}/AddNetSchool`, {
            method: 'POST', // Set the method to POST
            headers: {
                'Content-Type': 'application/json', // Specify the content type
            },
            body: JSON.stringify(requestBody) // Convert the request body to JSON
        });

        // Check if the response is OK (status code 200-299)
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Parse the JSON response
        const data = await response.json();
        return data; // Return the response data

    } catch (error) {
        console.error('Error adding net school:', error);
        throw error; // Rethrow the error for further handling if needed
    }
};