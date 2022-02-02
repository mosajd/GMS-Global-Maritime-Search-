# GMS-Global Maritime Search

<h3>Porpuse</h3>
<p>This software is designed for this purpose to be a tool to simulate and calculate the cost and time of sailing through Northern Sea Route (NSR) and  Suez Canal Route (SCR).</p>

<h3>Introduction</h3>
<p>According to global warming, icebergs in the artic ocean is expected to melt in a few years. Due to the likely consequences, the maritime artic sea route pole would become available for vessel ships to sail across without utilizing specific equipment such as ice breakers.</p>
<p>Therefore, analyzing and comparing artic sea route passage with other routes can be considered for many businesses particularly for freight companies.</p>
<p>GMS (Global Maritime Search) software which is one of the teamwork projects for 'Modelling and Design of Complex Systems' course from the master program of 'Engineering Technology for Strategy and Security - Strategos' at the University of Genova is designed to model this scenario.</p>
<h3>Model</h3>
<p>This model currently evaluating, analyzing, and comparing two routes: Suez Canal Route (SCR) and Northern Sea Route (NSR), considering that NSR is free of icebergs and is accessible at most times of the year.</p>
<p>This model calculates both Time and Cost for each desired voyage in both <b>deterministic</b> and <b>stochastic (probabilistic)</b> simulations.</p>
<h4>Input Deterministic Parameters</h4>
<ul>
  <li>Distance (between two ports)</li>
  <li>Average shipping speed</li>
<li>Vessel type (TEU, load capacity, dimensions, tank capacity, year of construction, crew, engine power, fuel consumption, price, and so on.)</li>
<li>Vessel costs (Services & maintenance, annual capital cost and depreciation, insurances, and crew salary</li>
  <li>Cargo (Type, value, weight, and insurance cost)</li>
<li>Time (Bureaucracy and administrative issues, the dwell time in ports, the average delay for bunkering)</li>
  <li>Fuel (Type and price for each route)</li>
  <li>Environmental cost (cost of air pollution and cost of global warming)</li>
</ul>
<h4>Input Stochastic Parameters</h4>
<ul>
<li>Fuel price (mean and standard deviation price for each route based on the normal distribution)</li>
<li>Weather conditions could affect shipping time and delay. For this parameter mean and standard deviation in terms of days are defined based on the normal distribution.</li>
<li>Wind and currents could affect shipping speed. For this parameter mean and standard deviation in terms of shipping speed are defined based on the normal distribution.</li>
</ul>
<p>All stochastic parameters in this model are created according to the Monte Carlo method and then applied to outputs.</p>

