using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace PWPClient
{
    public class Users
    {

    }


    public class RESTfulHandler
    {
        public String HTTPGet(String URI)
        {
            String resp = "";
            HttpWebRequest request = (HttpWebRequest)WebRequest.Create(URI);
            request.AutomaticDecompression = DecompressionMethods.GZip;
            try
            {
                using (HttpWebResponse response = (HttpWebResponse)request.GetResponse())
                using (Stream stream = response.GetResponseStream())
                using (StreamReader reader = new StreamReader(stream))
                {
                    resp = reader.ReadToEnd();
                }
            } 
            catch (WebException e)
            {
                MessageBox.Show("ERROR");
            }

            return resp;
        }

        public void HTTPPut(String URI, String JSON)
        {
            HttpWebRequest request = (HttpWebRequest)WebRequest.Create(URI);
            request.Method = "PUT";
            request.ContentType = "application/json";
            JObject newdata = new JObject(
                                new JProperty("password", "Newton-King"),
                                new JProperty("email", "test@yahoo.com"),
                                new JProperty("mobile", "0414868688"),
                                new JProperty("website", "asdasdsad.asdasd.com"),
                                new JProperty("isAdmin", "1"),
                                new JProperty("updatedBy", "3")
                                
                                );
            Console.WriteLine(newdata.ToString());

            using (var streamWriter = new StreamWriter(request.GetRequestStream()))
            {
            }
            var httpResponse = (HttpWebResponse)request.GetResponse();
            using (var streamReader = new StreamReader(httpResponse.GetResponseStream()))
            {
                var responseText = streamReader.ReadToEnd();
                MessageBox.Show(responseText.ToString());
            }
        }
    }
}
