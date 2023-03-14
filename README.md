<h1>Pyscramte</h1>

<p>A powerful web scraper for hackers and malicious coders.</p>

<h2>Usage</h2>

<p>Install the required packages:</p>

<pre><code class="language-bash">pip install -r requirements.txt
</code></pre>

<p>Run the script with the desired URL and output file name as arguments:</p>

<pre><code class="language-bash">python pyscramte.py [-h] [-d DIRECTORY] [-t TIMEOUT] [-v] url
</code></pre>

<p>You will be prompted to enter the URL of the webpage you want to scrape. The output file name is optional, and the default output file name is <code>output.txt</code>.</p>

<p>The script will launch a Chrome browser in headless mode and extract all links from the webpage source. The links will be saved to the specified output file.</p>

<h2>Requirements</h2>

<ul>
  <li>Python 3.6+</li>
  <li>Selenium</li>
  <li>Google Chrome (or any other browser supported by Selenium)</li>
</ul>

<h2>Contributing</h2>

<p>Contributions are welcome! Please open an issue or pull request if you have any suggestions or improvements.</p>

<h2>License</h2>

<p>This project is licensed under the MIT License. See the <a href="LICENSE">LICENSE</a> file for details.</p>
