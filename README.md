# POCSAG-Decoder
 <p>This decoder is loosly based on <a href="https://habr.com/en/articles/438906/">this article</a> and adds some extra functionality:
 <ul>
  <li>Address Decoding</li>
  <li>Continuous Resynchronization</li>
  <li>Verbose data display</li>
</ul>
</p>
<p>I wrote this primarially to make sure that the POGSAG encoder in <a href="https://github.com/jgromes/RadioLib/blob/master/src/protocols/Pager/Pager.cpp">radiolib</a> was doing what it should and also get get a better understanding of exactly how pagers work.</p>

<h2>Data Preparation</h2>

<img src="gqrx.png" alt="" style="width:400px;" class="imgholder">
<p class="left"><i>Pager Transmission in GQRX</i></p>

<ol type="1">
  <li>Use GQRX or other SDR software to record a pager transmission as a WAV file.</li>
  <li>Apply a low pass filter in Audacity and trim the result to start just before the first positive zero crossing and end after the bit period after the last zero crossing. </li>
  <li>Run the python script.</li>
</ol>

<img src="filter.png" alt="" style="width:400px;" class="imgholder">
<p class="left"><i>Example Low Pass Filter in Audacity</i></p>

<h2>Address Decoding</h2>
<p>As many references state, the CAP-CODE address is split in two parts: The first 19 bits come from the address field of the address codeword and the last three bits come from the position of the address codeword in the frame. What I could not find was how to translate the position of the address codeword into bits &mdash; there are 16 possible positions within each batch, but three bits distinguish only eight possibilities. Naively, I expected these bits to be encoded such that an address codeword transmitted immedietly after a sync word would have LSB 000 and an address codeword transmitted with seven idle codewords between the sync word and address word would have an LSB of 111. I expected this to be the case since I expected this to minimize air time (at most, seven idle words would be transmitted before the address is transmitted). This is <i>not</> how it works!</p>
 
<p>What actually happens is that the address word is offset from the sync word by 2x the idle words as the LSB of the address. As such, an address with an LSB of 001 has two idle codewords between it and the sync word and an address with an LSB of 111 has fourteen idle codewords between it and the sync word. This is clearly shown in the source code for radiolib's pager library, but I don't see it in other references that come up on Google.</p>

<h2>Continuous Resynchronization</h2>
<p>The example I started with <a href="https://habr.com/en/articles/438906/">here</a> samples the waveform based on assuming its bit period synchronized only to the first zero crossing. I had enough offset in my data compared to the ideal rate of 1200 bps that I was no longer sampling at the right point on the waveform after about 3/4 of a transmission. To solve this, I added some code to resynchonize the sampling points to positive zero crossings.</p>

<h2>Verbose Data Display</h2>
