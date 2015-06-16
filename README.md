# Py_XPPCALL
<div style="text-align:justify">

<a href="http://www.math.pitt.edu/~bard/xpp/xpp.html">XPPAUT</a> is a great software for the analysis of dynamical systems. Many mathematical models have been implemented with XPPAUT (*.ODE file format) [search for examples at&nbsp;<a href="http://senselab.med.yale.edu/modeldb/">http://senselab.med.yale.edu/modeldb/</a>]. These implementations could be used to reproduce computational experiments and to quickly test ideas related to them. For instance, one could perform the sensitivity analysis of model's parameters&nbsp;or parameters' space searches. However, due to the graphical nature of XPPAUT,&nbsp;the batch modification of parameters of these models is problematic.&nbsp;
<div><br>
</div>
<div>Here I describe the solution for this problem using simple python module <b>Py_XPPCALL</b> that I have written to interface with XPPAUT. It allows you to batch-modify model's parameters and returns corresponding solutions. An analogous software exists, <a href="https://github.com/jsnowacki/xppy" style="line-height:1.5;background-color:transparent">https://github.com/jsnowacki/xppy</a>, however little documentation is available.</div>
<div><br>
</div>
<div>Py_XPPCALL is easy to use and does not require installation. Simply put <b><a href="https://sites.google.com/site/ilyaprokin/py_xppcall-a-python-binding-to-xppaut/xppcall.py?attredirects=0">xppcall.py</a></b> to your python path or current folder.</div>
<h3>An example of usage with Hodgkin-Huxley neuron model for numerical optimization</h3>
<div>I extracted the ODE source code of Hodgkin-Huxley model &nbsp;from the example at the website of XPPAUT&nbsp;<a href="http://www.math.pitt.edu/~bard/bardware/tut/newstyle.html#hh">http://www.math.pitt.edu/~bard/bardware/tut/newstyle.html#hh</a>. I saved it as <a href="https://sites.google.com/site/ilyaprokin/py_xppcall-a-python-binding-to-xppaut/hh.ode?attredirects=0">hh.ode</a>. I put it to the same folder where I have <a href="https://sites.google.com/site/ilyaprokin/py_xppcall-a-python-binding-to-xppaut/xppcall.py?attredirects=0">xppcall.py</a> and ran python from there.&nbsp;</div>
<div><br>
</div>
<div><i>Note:</i> Links to all the files used here, including the code of the example, are given at the end of this page.</div>

</div>

<div><br>
</div>
<hr>
<div><br>
</div>
<div>
<pre style="line-height:16.25px;color:rgb(0,0,0)"><span style="color:rgb(136,136,136)">## Py_XPPCALL Example</span>

<span style="color:rgb(136,136,136)"># import some modules including Py_XPPCALL</span>
<span style="color:rgb(0,136,0);font-weight:bold">import</span> <span style="color:rgb(14,132,181);font-weight:bold">matplotlib.pylab</span> <span style="color:rgb(0,136,0);font-weight:bold">as</span> <span style="color:rgb(14,132,181);font-weight:bold">plt</span>
<span style="color:rgb(0,136,0);font-weight:bold">import</span> <span style="color:rgb(14,132,181);font-weight:bold">numpy</span> <span style="color:rgb(0,136,0);font-weight:bold">as</span> <span style="color:rgb(14,132,181);font-weight:bold">np</span>
<span style="color:rgb(0,136,0);font-weight:bold">from</span> <span style="color:rgb(14,132,181);font-weight:bold">xppcall</span> <span style="color:rgb(0,136,0);font-weight:bold">import</span> <span>xpprun</span><span>,</span> <span>read_pars_values_from_file</span>

<span style="color:rgb(136,136,136)"># Let's check what are the parameters of the model</span>
<span>pars</span> <span style="color:rgb(51,51,51)">=</span> <span>read_pars_values_from_file</span><span>(</span><span style="background-color:rgb(255,240,240)">'hh.ode'</span><span>)</span>
<span style="color:rgb(0,136,0);font-weight:bold">print</span> <span>pars</span>
<br></pre>
<pre><font color="#000000"><span style="line-height:16.25px">Out[]:&nbsp;</span></font></pre>
<pre><font color="#000000"><span style="line-height:16.25px">
{'c': '1',
 'gk': '36',
 'gl': '.3',
 'gna': '120',
 'i': '0',
 'vk': '-77',
 'vl': '-54.4',
 'vna': '50'}</span></font></pre>
<pre style="line-height:16.25px;color:rgb(0,0,0)"><span style="color:rgb(136,136,136)"># Note: XPPAUT is not case sensitive. In Py_XPPCALL, the names of parameters and variables were chosen to be in lower case.</span>

<span style="color:rgb(136,136,136)"># Let's plot solution for membrane potential with parameters specified in .ODE file</span>
<span>npa</span><span>,</span> <span>vn</span> <span style="color:rgb(51,51,51)">=</span> <span>xpprun</span><span>(</span><span style="background-color:rgb(255,240,240)">'hh.ode'</span><span>,</span> <span>clean_after</span><span style="color:rgb(51,51,51)">=</span><span style="color:rgb(0,112,32)">True</span><span>)</span>
<span>plt</span><span style="color:rgb(51,51,51)">.</span><span>figure</span><span>()</span>
<span>plt</span><span style="color:rgb(51,51,51)">.</span><span>plot</span><span>(</span><span>npa</span><span>[:,</span><span style="color:rgb(0,0,221);font-weight:bold">0</span><span>],</span> <span>npa</span><span>[:,</span> <span style="color:rgb(0,0,221);font-weight:bold">1</span><span style="color:rgb(51,51,51)">+</span><span>vn</span><span style="color:rgb(51,51,51)">.</span><span>index</span><span>(</span><span style="background-color:rgb(255,240,240)">'v'</span><span>)])</span>
<br></pre>
<pre style="line-height:16.25px;color:rgb(0,0,0)"><pre style="color:rgb(97,97,97);line-height:21px"><font color="#000000"><span style="line-height:16.25px">Out[]:</span></font></pre><div style="display:block;text-align:left"><a href="https://sites.google.com/site/ilyaprokin/py_xppcall-a-python-binding-to-xppaut/1.png?attredirects=0" imageanchor="1"><img border="0" src="https://sites.google.com/site/ilyaprokin/py_xppcall-a-python-binding-to-xppaut/1.png"></a></div>
<span style="color:rgb(136,136,136)"># Let's modify constant input current</span>
<span>npa</span><span>,</span> <span>vn</span> <span style="color:rgb(51,51,51)">=</span> <span>xpprun</span><span>(</span><span style="background-color:rgb(255,240,240)">'hh.ode'</span><span>,</span> <span>parameters</span><span style="color:rgb(51,51,51)">=</span><span>{</span><span style="background-color:rgb(255,240,240)">'i'</span><span>:</span><span style="color:rgb(102,0,238);font-weight:bold">20.0</span><span>},</span> <span>clean_after</span><span style="color:rgb(51,51,51)">=</span><span style="color:rgb(0,112,32)">True</span><span>)</span>
<span>plt</span><span style="color:rgb(51,51,51)">.</span><span>figure</span><span>()</span>
<span>plt</span><span style="color:rgb(51,51,51)">.</span><span>plot</span><span>(</span><span>npa</span><span>[:,</span><span style="color:rgb(0,0,221);font-weight:bold">0</span><span>],</span> <span>npa</span><span>[:,</span> <span style="color:rgb(0,0,221);font-weight:bold">1</span><span style="color:rgb(51,51,51)">+</span><span>vn</span><span style="color:rgb(51,51,51)">.</span><span>index</span><span>(</span><span style="background-color:rgb(255,240,240)">'v'</span><span>)])</span>
<br></pre>
<pre style="line-height:16.25px;color:rgb(0,0,0)"><pre style="color:rgb(97,97,97);line-height:21px"><font color="#000000"><span style="line-height:16.25px">Out[]:</span></font></pre><div style="display:block;text-align:left"><a href="https://sites.google.com/site/ilyaprokin/py_xppcall-a-python-binding-to-xppaut/2.png?attredirects=0" imageanchor="1"><img border="0" src="https://sites.google.com/site/ilyaprokin/py_xppcall-a-python-binding-to-xppaut/2.png"></a></div>

<span style="color:rgb(136,136,136)"># Example of an optimization using fmin from SciPy</span>
<span style="color:rgb(0,136,0);font-weight:bold">from</span> <span style="color:rgb(14,132,181);font-weight:bold">scipy.optimize</span> <span style="color:rgb(0,136,0);font-weight:bold">import</span> <span>fmin</span>

<span style="color:rgb(136,136,136)"># define desired V graph</span>
<span>target_v</span> <span style="color:rgb(51,51,51)">=</span> <span style="color:rgb(51,51,51)">-</span><span style="color:rgb(102,0,238);font-weight:bold">80.0</span><span style="color:rgb(51,51,51)">+</span><span style="color:rgb(0,0,221);font-weight:bold">20</span><span style="color:rgb(51,51,51)">*</span><span>npa</span><span>[:,</span><span style="color:rgb(0,0,221);font-weight:bold">0</span><span>]</span><span style="color:rgb(51,51,51)">*</span><span>(</span><span>np</span><span style="color:rgb(51,51,51)">.</span><span>sign</span><span>(</span><span style="color:rgb(51,51,51)">-</span><span>npa</span><span>[:,</span><span style="color:rgb(0,0,221);font-weight:bold">0</span><span>]</span><span style="color:rgb(51,51,51)">+</span><span style="color:rgb(0,0,221);font-weight:bold">4</span><span>)</span><span style="color:rgb(51,51,51)">+</span><span style="color:rgb(0,0,221);font-weight:bold">1</span><span>)</span>
<span>plt</span><span style="color:rgb(51,51,51)">.</span><span>figure</span><span>()</span>
<span>plt</span><span style="color:rgb(51,51,51)">.</span><span>plot</span><span>(</span><span>npa</span><span>[:,</span><span style="color:rgb(0,0,221);font-weight:bold">0</span><span>],</span> <span>target_v</span><span>)</span>
<br></pre>
<pre style="line-height:16.25px;color:rgb(0,0,0)"><pre style="color:rgb(97,97,97);line-height:21px"><font color="#000000"><span style="line-height:16.25px">Out[]:</span></font></pre><pre style="color:rgb(97,97,97);line-height:21px"><font color="#000000"><span style="line-height:16.25px"><div style="display:block;text-align:left"><a href="https://sites.google.com/site/ilyaprokin/py_xppcall-a-python-binding-to-xppaut/3.png?attredirects=0" imageanchor="1"><img border="0" src="https://sites.google.com/site/ilyaprokin/py_xppcall-a-python-binding-to-xppaut/3.png"></a></div><br></span></font></pre>
<span style="color:rgb(136,136,136)"># define objective_func we want to minimize</span>
<span style="color:rgb(0,136,0);font-weight:bold">def</span> <span style="color:rgb(0,102,187);font-weight:bold">objective_func</span><span>(</span><span>x</span><span>,</span> <span>target</span><span style="color:rgb(51,51,51)">=</span><span>target_v</span><span>):</span>
    <span style="color:rgb(0,136,0);font-weight:bold">try</span><span>:</span>
        <span>npa</span><span>,</span> <span>vn</span> <span style="color:rgb(51,51,51)">=</span> <span>xpprun</span><span>(</span><span style="background-color:rgb(255,240,240)">'hh.ode'</span><span>,</span> <span>parameters</span><span style="color:rgb(51,51,51)">=</span><span>{</span><span style="background-color:rgb(255,240,240)">'i'</span><span>:</span><span>x</span><span>[</span><span style="color:rgb(0,0,221);font-weight:bold">0</span><span>]},</span> <span>clean_after</span><span style="color:rgb(51,51,51)">=</span><span style="color:rgb(0,112,32)">True</span><span>)</span>
        <span>computed</span> <span style="color:rgb(51,51,51)">=</span> <span>npa</span><span>[:,</span> <span style="color:rgb(0,0,221);font-weight:bold">1</span><span style="color:rgb(51,51,51)">+</span><span>vn</span><span style="color:rgb(51,51,51)">.</span><span>index</span><span>(</span><span style="background-color:rgb(255,240,240)">'v'</span><span>)]</span>
        <span style="color:rgb(0,136,0);font-weight:bold">return</span> <span>np</span><span style="color:rgb(51,51,51)">.</span><span>mean</span><span>(</span> <span>(</span><span>computed</span><span style="color:rgb(51,51,51)">-</span><span>target</span><span>)</span><span style="color:rgb(51,51,51)">**</span><span style="color:rgb(0,0,221);font-weight:bold">2</span> <span>)</span>
    <span style="color:rgb(0,136,0);font-weight:bold">except</span><span>:</span>
        <span style="color:rgb(0,136,0);font-weight:bold">return</span> <span style="color:rgb(102,0,238);font-weight:bold">1e10</span> <span style="color:rgb(136,136,136)"># return huge error if something went wrong</span>

<span>xopt</span> <span style="color:rgb(51,51,51)">=</span> <span>fmin</span><span>(</span><span>objective_func</span><span>,</span> <span>[</span><span style="color:rgb(102,0,238);font-weight:bold">20.0</span><span>])</span> <span style="color:rgb(136,136,136)"># find new parameters</span>
<span>npa</span><span>,</span> <span>vn</span> <span style="color:rgb(51,51,51)">=</span> <span>xpprun</span><span>(</span><span style="background-color:rgb(255,240,240)">'hh.ode'</span><span>,</span> <span>parameters</span><span style="color:rgb(51,51,51)">=</span><span>{</span><span style="background-color:rgb(255,240,240)">'i'</span><span>:</span><span>xopt</span><span>[</span><span style="color:rgb(0,0,221);font-weight:bold">0</span><span>]},</span> <span>clean_after</span><span style="color:rgb(51,51,51)">=</span><span style="color:rgb(0,112,32)">True</span><span>)</span>
<span>plt</span><span style="color:rgb(51,51,51)">.</span><span>figure</span><span>()</span>
<span>plt</span><span style="color:rgb(51,51,51)">.</span><span>plot</span><span>(</span><span>npa</span><span>[:,</span><span style="color:rgb(0,0,221);font-weight:bold">0</span><span>],</span> <span>npa</span><span>[:,</span> <span style="color:rgb(0,0,221);font-weight:bold">1</span><span style="color:rgb(51,51,51)">+</span><span>vn</span><span style="color:rgb(51,51,51)">.</span><span>index</span><span>(</span><span style="background-color:rgb(255,240,240)">'v'</span><span>)],</span> <span>label</span><span style="color:rgb(51,51,51)">=</span><span style="background-color:rgb(255,240,240)">'fit'</span><span>)</span>
<span>plt</span><span style="color:rgb(51,51,51)">.</span><span>plot</span><span>(</span><span>npa</span><span>[:,</span><span style="color:rgb(0,0,221);font-weight:bold">0</span><span>],</span> <span>target_v</span><span>,</span> <span>label</span><span style="color:rgb(51,51,51)">=</span><span style="background-color:rgb(255,240,240)">'target'</span><span>)</span>
<span>plt</span><span style="color:rgb(51,51,51)">.</span><span>legend</span><span>()</span></pre>
<pre style="line-height:16.25px;color:rgb(0,0,0)"><span><br></span></pre>
<pre style="line-height:16.25px;color:rgb(0,0,0)"><span>Out[]:</span></pre>
<pre style="line-height:16.25px;color:rgb(0,0,0)"><span><div style="display:block;text-align:left"><a href="https://sites.google.com/site/ilyaprokin/py_xppcall-a-python-binding-to-xppaut/4.png?attredirects=0" imageanchor="1"><img border="0" src="https://sites.google.com/site/ilyaprokin/py_xppcall-a-python-binding-to-xppaut/4.png"></a></div></span></pre>
<h3>Congrats! We got a pretty good fit.</h3>
</div>

