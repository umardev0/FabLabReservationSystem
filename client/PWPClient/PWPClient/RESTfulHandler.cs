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

        public void HTTPPut(String URI, JObject JSONData)
        {
            HttpWebRequest request = (HttpWebRequest)WebRequest.Create(URI);
            request.Method = "PUT";
            request.ContentType = "application/json";
            
            byte[] byteArray = Encoding.UTF8.GetBytes(JSONData.ToString());
            try
            {
                request.ContentLength = byteArray.Length;
                Stream streamRequest = request.GetRequestStream();
                streamRequest.Write(byteArray, 0, byteArray.Length);
                streamRequest.Close();
                HttpWebResponse response = (HttpWebResponse)request.GetResponse();
                MessageBox.Show("Status Code: " + (int)response.StatusCode);
            }
            catch (WebException e)
            {
                MessageBox.Show("WebException:" +e.Status+ "With response:" +e.Message);

            }

        }
        public void HTTPPost(String URI, JObject JSONData)
        {
            HttpWebRequest request = (HttpWebRequest)WebRequest.Create(URI);
            byte[] byteArray = Encoding.UTF8.GetBytes(JSONData.ToString());

            request.Method = "POST";
            request.ContentType = "application/json";
            request.ContentLength = byteArray.Length;
            Console.WriteLine(JSONData.ToString());
            try
            {
                Stream streamRequest = request.GetRequestStream();
                streamRequest.Write(byteArray, 0, byteArray.Length);
                streamRequest.Close();
                HttpWebResponse response = (HttpWebResponse)request.GetResponse();
                MessageBox.Show("Status Code: " + (int)response.StatusCode);
            }
            catch (WebException e)
            {
                MessageBox.Show("WebException:" + e.Status + "With response:" + e.Message);

            }
        }

        public void HTTPDelete(String URI)
        {
            HttpWebRequest request = (HttpWebRequest)WebRequest.Create(URI);
            request.Method = "DELETE";
            request.ContentType = "application/json";

            try
            {
                HttpWebResponse response = (HttpWebResponse)request.GetResponse();
                MessageBox.Show("Status Code: " + (int)response.StatusCode);
            }
            catch (WebException e)
            {
                MessageBox.Show("WebException:" + e.Status + "With response:" + e.Message);

            }

        }
    }
}
