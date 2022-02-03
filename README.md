# GMS-Global Maritime Search
<h2>Table of Contents</h2>
<ul>
  <li><a href=#porpuse>Porpuse</a></li>
  <li><a href=#introduction>Introduction</a></li>
  <li><a href=#model>Model</a></li>
  <li><a href=#tutorial>Tutorial</a>
    <ul>
      <li><a href=#routes>Routes</a></li>
      <li><a href=#vessel>Vessel</a></li>
      <li><a href=#cargo>Cargo</a></li>
      <li><a href=#time>Time</a></li>
      <li><a href=#fuel>Fuel</a></li>
      <li><a href=#environment>Environment</a></li>
      <li><a href=#cost>Cost</a></li>
      <li><a href=#stochastic>Stochastic</a></li>
    </ul>
  </li>
  <li><a href=#>Futute Studies</a>
  <li><a href=#>How to run the software</a>
  
</ul>
<h2>Porpuse</h2>
<p>This software is designed for this purpose to be a tool to simulate and calculate the cost and time of sailing through Northern Sea Route (NSR) and  Suez Canal Route (SCR).</p>

<h2>Introduction</h2>
<p>According to global warming, icebergs in the artic ocean is expected to melt in a few years. Due to the likely consequences, the maritime artic sea route pole would become available for vessel ships to sail across without utilizing specific equipment such as ice breakers.</p>
<p>Therefore, analyzing and comparing artic sea route passage with other routes can be considered for many businesses particularly for freight companies.</p>
<p>GMS (Global Maritime Search) software which is one of the teamwork projects for 'Modelling and Design of Complex Systems' course from the master program of 'Engineering Technology for Strategy and Security - Strategos' at the University of Genova is designed to model this scenario.</p>
<h2>Model</h2>
<p>This model currently evaluating, analyzing, and comparing two routes: Suez Canal Route (SCR) and Northern Sea Route (NSR), considering that NSR is free of icebergs and is accessible at most times of the year.</p>
<p>This model calculates both Time and Cost for each desired voyage in both <b>deterministic</b> and <b>stochastic (probabilistic)</b> simulations.</p>
<h3>Input Deterministic Parameters</h3>
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
<h3>Input Stochastic Parameters</h3>
<ul>
<li>Fuel price (mean and standard deviation price for each route based on the normal distribution)</li>
<li>Weather conditions could affect shipping time and delay. For this parameter mean and standard deviation in terms of days are defined based on the normal distribution.</li>
<li>Wind and currents could affect shipping speed. For this parameter mean and standard deviation in terms of shipping speed are defined based on the normal distribution.</li>
</ul>
<p>All stochastic parameters in this model are created according to the Monte Carlo method and then applied to outputs.</p>
<p>The relation between the parameters are depicted in the following pictures.</p>
<figure>
<p>In this picture you can see how both deterministic and stochastic parameters affect on the time of voyage.</p>
<img src="https://github.com/mosajd/GMS-Global-Maritime-Search-/blob/main/time.jpg" alt="time">
</figure><br>
<figure>
<p>And in this one you see how both deterministic and stochastic parameters in this software affect on the cost of voyage.</p>
<img src="https://github.com/mosajd/GMS-Global-Maritime-Search-/blob/main/cost.jpg" alt="time">
</figure>
<h2>Tutorial</h2>
<h3>Routes</h3>
<p>1 - At the first you should define both departure and arrival ports.</p>
<p>2 - Define one of the maritime route. (for this version only NSR and SCR are activated)</p>
<p>3 - In this step, maritime distance between departure and arrival ports is shown. This distance found from <a href='https://www.aquaplot.com/explorer'>Aquaplot website</a> and compared with the given distances by <a href='https://www.portworld.com/map'>Portworld website</a>. You can also change the distance here and all of the next calculation will be done base on the given distance in this box.</p>
<p>4 - The software recommends you the average shipping speed, but it is better to change it if you have more accurate maritime shipping speed for this route.</p>
<p>Finally, based on the all given data, the shipping time is calculated.</p>
<figure>
<img src="https://github.com/mosajd/GMS-Global-Maritime-Search-/blob/main/tutorial_images/tutorial_routes.jpg" alt="tutorial routes">
</figure><br>
<p>You can see the shipping route on the map by pushing the "Show on the map" button. This map is created by the <a href='https://python-visualization.github.io/folium/'>Folium</a> package inside the python to show the animated route.</p>
<p>By using the 'Measure Distances and Areas' inside the map you can measure the route manualy.</p>
<figure>
<img src="https://github.com/mosajd/GMS-Global-Maritime-Search-/blob/main/tutorial_images/tutorial_map.jpg" alt="tutorial map">
</figure><br>
<h3>Vessel</h3>
<p>5 - Select one of the vessels from the list that their parameters found from <a href='https://services-webdav.cbs.dk/doc/CBS.dk/Arctic%20Shipping%20-%20Commercial%20Opportunities%20and%20Challenges.pdf'>Arctic Shipping Commercial Opportunites and Challenges</a>.</p>
<b>Note: </b>Fuel tank capacities of the given vessel in the list are assumed and not found from the reference.
<p>You can also define another parameters for the vessel by selecting the 'NEW'. 'TEU', 'Gross Tonnage', 'DWT', 'Vessel Price' and 'Fuel Consumption' are affected in the next calculations. So you can skip other parameters for the vessel.</p>
<p>6 - Based on this <a href='https://www.researchgate.net/profile/Masahiko-Furuichi/publication/246545438_Cost_Analysis_of_the_Northern_Sea_Route_NSR_and_the_Conventional_Route_Shipping/links/02e7e51d97c39e870e000000/Cost-Analysis-of-the-Northern-Sea-Route-NSR-and-the-Conventional-Route-Shipping.pdf'>reference</a>, an annual maintenance cost can be determined proportional (1.095% / year) to the ship building cost, whatever the ship types vary. Maintenance cost is comprised of article cost of ship, lubricant cost, dock cost and spare parts cost. But you can change the coefficient and it will be implemented in voyage cost.</p>
<p>7 - Annual Capital Cost for the vessel is estimated by multiplying the capital costs of building the vessel to the given coefficient found from <a href='https://www.tandfonline.com/doi/abs/10.1080/03088839.2018.1473656?casa_token=Bdw-vSRtWGMAAAAA%3A7-0I81pWz12l_Evn90Kof1_pe9tbLLPbKLmCcZuXtYGON9PS_fMUktBRS8znEaVFH1BBLbJO4SBRDg&journalCode=tmpm20'>this reference.</a></p>
<p>8 - The ocean-going ship is generally required to purchase both H&M and P&I insurance. However, insurance cost estimation is one of the most difficult task to achieve, because insurance market transactions are not usually disclosed to the public due to the nature of the insurance business.</p>
<p>Based on the reaserch from <a href='https://www.researchgate.net/profile/Masahiko-Furuichi/publication/246545438_Cost_Analysis_of_the_Northern_Sea_Route_NSR_and_the_Conventional_Route_Shipping/links/02e7e51d97c39e870e000000/Cost-Analysis-of-the-Northern-Sea-Route-NSR-and-the-Conventional-Route-Shipping.pdf'>this article</a>, the software recommends following calculation for annual vessel insurance cost:</p>
<pre>Annual insurance cost = 0.00343 * Vessel Price</pre>
<p>9 - Here you can define the Average salary for the crew per month.</p>
<figure>
<img src="https://github.com/mosajd/GMS-Global-Maritime-Search-/blob/main/tutorial_images/tutorial_vessel.jpg" alt="tutorial vessel">
</figure><br>
<h3>Cargo</h3>
<p>10 - In this section you can define the value of the cargo, that affects on the cargo insurance cost.</p>
<p>11 - Here you can define the cargo insurance by defining the percentage of the value of cargo.</p>
<figure>
<img src="https://github.com/mosajd/GMS-Global-Maritime-Search-/blob/main/tutorial_images/tutorial_cargo.jpg" alt="tutorial cargo">
</figure><br>
<h3>Time</h3>
<p>12 - You can difine the estimated delay time for Bureaucracy and administrative.</p>
<p>13 - Port dwell time is the amount of time which cargo or ships spend within the port. This model recommends dwelling time based on the TEU vessel parameter that found from <a href='https://www.tandfonline.com/doi/abs/10.1080/03088839.2018.1473656?needAccess=true&journalCode=tmpm20'>this article</a>.</p>
<p>14 - In this part the bunkering delay time for refueling is calculated based on the 'total fuel consumption on the voyage', 'vessel fuel capacity' and 'average delayed time in bunkering ports'.</p>
<p>At the end, 'shipping time' added to the 'dwell time', 'bunkering time' and 'Bureaucracy and administrative dely time' to estimate total shipping time for this voyage.</p>
<figure>
<img src="https://github.com/mosajd/GMS-Global-Maritime-Search-/blob/main/tutorial_images/tutorial_time.jpg" alt="tutorial time">
</figure><br>
<h3>Fuel</h3>
<p>15 - You should select one of the fuel type for the vessel that affects on the cost, time (bunkering time) and environmental cost.</p>
<p>In the Fuel Cost box, the 'Total Fuel Price in this voyage' in respect of 'Fuel Price' and 'Fuel Consumption' is calculated.</p>
<figure>
<img src="https://github.com/mosajd/GMS-Global-Maritime-Search-/blob/main/tutorial_images/tutorial_fuel.jpg" alt="tutorial fuel">
</figure><br>
<h3>Environment</h3>
<p>In this tab, by pushing the 'Calculate Environment Cost', 'Cost of Air Pollution (CAP)' and 'Cost of Global Warming (CGW) for this voyage is estimated. The environmental cost in respect of 'route', 'type of oil', 'amount of fuel consumption in the voyage' and 'TEU vessel parameter' derived from <a href='https://www.sciencedirect.com/science/article/abs/pii/S0308597X20301792'>this article</a>.</p>
<figure>
<img src="https://github.com/mosajd/GMS-Global-Maritime-Search-/blob/main/tutorial_images/tutorial_environment.jpg" alt="tutorial Environment">
</figure><br>
<h3>Cost</h3>
<p>16 - Port dues cost usually consists of including port entry due, berthing due and line-handling charge in total for each port entry. The following formula found from <a href='https://www.researchgate.net/profile/Masahiko-Furuichi/publication/246545438_Cost_Analysis_of_the_Northern_Sea_Route_NSR_and_the_Conventional_Route_Shipping/links/02e7e51d97c39e870e000000/Cost-Analysis-of-the-Northern-Sea-Route-NSR-and-the-Conventional-Route-Shipping.pdf'>this article</a> and applied in this model:</p>
<pre>Port Dues Cost = $0.428 / GT / call</pre>
<p>17 - The SCR shipping may need to bear a significant disadvantage of piracy risk of Somalia. As Ship & Ocean Foundation (SOF) and Aden Emergency reported the annual piracy insurance for each route is calculated in the following way:</p>
<pre>Annual piracy insurance cost for NSR = $10 / GT / year</pre>
<pre>Annual piracy insurance cost for SCR = $40 / TEU / year</pre>
<p>In the next boxes, the other costs based on the total days of shipping is calculated seperately and at the end added togother to find total cost of this voyage.</p>
<figure>
<img src="https://github.com/mosajd/GMS-Global-Maritime-Search-/blob/main/tutorial_images/tutorial_cost.jpg" alt="tutorial Cost">
</figure><br>
<p>By pushing the 'Show on the Pie Chart' button, the percentage of the total cost on the pie chart in a new window will be showed.</p>
<figure>
<img src="https://github.com/mosajd/GMS-Global-Maritime-Search-/blob/main/tutorial_images/tutorial_pie_chart.jpg" alt="tutorial Pie Chart">
</figure><br>
<h3>Stochastic</h3>
<p>All of the calculations done so far were based on the deterministic inputs. But we know that in real life there are many stochastic parameters like fuel price and weather condition that signifantly affect the output. In this model the <a href='https://en.wikipedia.org/wiki/Monte_Carlo_method'>Monte Carlo</a> method is implemented to estimate the result of stochastic parameters on both cost and time.</p>
<h4>Fuel Price</h4>
<p>Fuel price usually follows the normal distribution that by defining the mean and standard deviation simulates.</p>
<h4>Weather</h4>
<p>In some maritime distance estimations usually use sea margin to account for foul weather, currents and to have a safety margin for consumption calculations. Sea margin is applied to distances when calculating fuel consumption. It will not affect the displayed distance values but it will affect travel time calculations and required fuel amounts. For example a distance of 1000 nm with a sea margin of 5 percent will be treated as an effective distance of 1050 nm.<br> 
In this simulation for the weather condition considered the margin percentage affected on the distance by generating random numbers based on the normal distribution.</p>
<h4>Wind and Currents</h4>
<p>Wind and Currents mostly affect on the shipping speed. In this simulation the shipping speed influenced by wind and currents considered as stochastic parameter that follow normal distribution.</p>
<h4>Simulation</h4>
<p>By defining the sample random number, random numbers generate and function for calculating time and cost is run. And finally the result will be shown on the histogram for both time and cost.</p>
<figure>
<img src="https://github.com/mosajd/GMS-Global-Maritime-Search-/blob/main/tutorial_images/tutorial_stochastic.jpg" alt="tutorial stochastic">
</figure><br>

