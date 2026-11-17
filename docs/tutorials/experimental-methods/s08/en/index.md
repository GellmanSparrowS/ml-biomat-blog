# ICP emission spectrometry: Turning elemental light into reliable concentrations

Source: https://ml-biomat.com/tutorials/experimental-methods/s08/en/
Language: en

Connect material release and composition with argon plasma, spectral separation, calibration and elemental mass accounting.

## What has a material left in a clear solution?

Place a calcium-containing polymer film in a buffer, wait several days, and remove it. The liquid may still look perfectly clear. Calcium could have entered the solution, or the main change could have remained at the surface. Neither appearance nor a simple mass measurement resolves the question easily: water uptake, retained salts and drying all affect the apparent mass. ICP optical emission spectrometry takes another route. It introduces a small portion of liquid into a hot argon plasma, collects the characteristic light emitted by its elements, and compares that signal with solutions of known concentration. For biomaterials research, this makes elemental release, inorganic filler composition, residual metals and changes in the surrounding medium separately measurable questions.

ICP stands for inductively coupled plasma and describes the source that supplies energy. OES means optical emission spectrometry; AES, atomic emission spectrometry, is also used for this family of measurements. The detector records light around selected wavelengths, while a calibration supplies the connection to concentration. A useful analogy is identifying instruments in an orchestra: pitch helps identify the source, whereas loudness requires a separate comparison. An elemental wavelength corresponds to an electronic energy difference. Its measured intensity also depends on how much sample reaches the plasma, the excitation conditions and the optical system. Identifying a line and quantifying an element are therefore related but distinct tasks.

Before measuring, complete the phrase “how much.” Calcium concentration in an extract, multiplied by the collected liquid volume, gives the calcium mass in that liquid. Dividing by the exposed material mass gives release per gram under the specified conditions. Completely digesting the material instead measures the calcium originally present in the solid. These experiments can use the same instrument while answering different questions. The complete numerical example in this chapter concerns a constructed, low-calcium polymer composite and its total calcium content on a dry-mass basis. The opening extraction example illustrates a different application; its time interval, liquid fraction and denominator remain distinct.

ICP-MS also uses an argon plasma, but its detection path is different. It transfers ions into a vacuum system and separates them by mass-to-charge ratio. ICP-OES collects photons and separates them by wavelength. Consequently, overlapping optical lines and background are central concerns in OES, whereas ions with overlapping mass-to-charge signals, including polyatomic ions, matter in MS. Method selection also depends on concentration, matrix, elements of interest, throughput and available facilities. OES is useful for many multielement composition measurements; very low concentrations or isotope questions call for assessment of an appropriate mass-spectrometric method.

The original molecules undergo substantial change before emission occurs. A calcium result does not by itself identify whether that calcium began in a phosphate, carbonate or soluble salt. Likewise, total chromium and chromium speciation are different measurements. Diffraction can help establish crystalline phases, infrared spectroscopy can examine functional groups, and sampling design determines whether a result concerns the surface or the bulk. Within such a study, ICP provides a clearly defined elemental mass account. Its value grows when the sampled fraction and the structural questions answered by other techniques are kept explicit.

## From flame colour to electrons in a plasma

In 1860, Kirchhoff and Bunsen published their work on chemical analysis through spectral observation. A salt introduced into a flame produces a colour, but passing the light through a slit and a prism reveals distinct bright lines. The prism spreads wavelengths in different directions, turning blended light into a signal with recognizable positions. The original schematic below illustrates this logic rather than reconstructing a particular historical instrument. Modern spectrometers commonly use gratings and electronic detectors, yet the principle remains recognizable: separate the light before comparing the contributions at different wavelengths.

Recognizing an element is easier than ensuring that its brightness measures its amount. Greenfield, Jones and Berry opened their 1964 paper by discussing suppression of calcium emission by phosphorus and aluminium in flames. The calcium had not disappeared; the efficiency with which it reached an emitting state had changed. They investigated hotter plasma sources, including high-frequency induction, whose sustained discharge did not require electrodes in the source. This history gives a useful experimental lesson. A new source was being developed partly because equal quantities could give unequal readings, and modern matrix correction still addresses variations in response efficiency.

![Original history and instrument schematic. A illustrates wavelength separation in the 1860 analysis; colours and geometry are explanatory. B illustrates the calcium suppression problem discussed in 1964; bar heights are conceptual. C shows droplet selection, drainage, concentric torch, RF coil and alternative axial/radial viewing paths; dimensions are not to scale.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/f18a5ba3d88071a037ae655a.svg?v=f18a5ba3d880)

Figure 1Original history and instrument schematic. A illustrates wavelength separation in the 1860 analysis; colours and geometry are explanatory. B illustrates the calcium suppression problem discussed in 1964; bar heights are conceptual. C shows droplet selection, drainage, concentric torch, RF coil and alternative axial/radial viewing paths; dimensions are not to scale.

A plasma is a gas containing many free electrons and ions. A radiofrequency current in a coil produces a changing magnetic field, which induces an electric field in the gas. Charged particles gain energy from that field and transfer it through collisions, helping sustain the plasma. Ignition establishes an initial population of charged particles; radiofrequency induction then supplies the continuing energy. Argon supports the discharge and transports the aerosol. The plasma is spatially structured rather than a furnace with one uniform temperature. Conditions along the central sample channel and in surrounding regions differ, explaining why gas flows, power and observation position affect the signal.

The liquid first becomes droplets in a nebulizer. A spray chamber removes larger droplets so that a finer aerosol reaches the plasma. Thus, liquid uptake and effective delivery to the emitting region are different quantities. Droplets lose solvent; the remaining material vaporizes and forms atoms, which can become excited or ionized. An excited atom or ion can emit a photon when an electron moves to a lower energy level. That lower level need not be the ground state. Several available transitions therefore give several lines for the same element, each with its own usefulness and possible interferences.

$$
\Delta E=E_{\mathrm{upper}}-E_{\mathrm{lower}}=h\nu=\frac{hc_0}{\lambda_0}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/03a061659f8f3f0ea28e1238.svg) | Energy difference or single-photon energy, J; also expressed in eV |
| ![Formula](https://ml-biomat.com/static/agent-math/d8ddb0fdc5f500d4eb915283.svg) | Upper- and lower-level energies for the transition, J |
| ![Formula](https://ml-biomat.com/static/agent-math/994427fe929fdf538d7c1be7.svg) | Planck constant, 6.62607015×10⁻³⁴ J s |
| ![Formula](https://ml-biomat.com/static/agent-math/5064898bae7c73820eaab47c.svg) | Optical frequency, s⁻¹ |
| ![Formula](https://ml-biomat.com/static/agent-math/b1fcf1f7db8487b0faca625a.svg) | Vacuum speed of light, 299792458 m/s; subscript 0 denotes vacuum |
| ![Formula](https://ml-biomat.com/static/agent-math/0a322167c6031b3ba1406fb9.svg) | Vacuum wavelength, m; 400 nm=400×10⁻⁹ m |

A photon carries the energy difference when an electron moves to a lower level. In vacuum, frequency is speed divided by wavelength. At 400 nm the result is 4.9661×10⁻¹⁹ J; dividing by 1.602176634×10⁻¹⁹ J per eV gives 3.09960496 eV. Air wavelengths require refractive-index conversion. This equation does not specify intensity.

The equation connects wavelength to the energy carried by one photon. A shorter wavelength corresponds to greater photon energy, but greater photon energy does not mean a more concentrated sample. Quantification compares the signal associated with a selected transition. For a vacuum wavelength of 400 nm, the photon energy is about 3.100 eV. A nanometre is one billionth of a metre; an electronvolt is a convenient unit for atomic-scale energies. Some line tables report air wavelengths. The distinction matters in precise energy conversion, so the numerical energy example uses a stated vacuum wavelength, while the calcium spectrum below uses a stated air wavelength.

Roman numerals in line names also carry a specific meaning. Ca I denotes neutral calcium atoms, and Ca II denotes singly ionized calcium. The numeral II is the second spectroscopic ionization stage, not the chemical notation for doubly charged calcium. Furthermore, it identifies the emitter in the plasma, not the oxidation state or molecular environment in the original specimen. The energetic source makes elemental comparison possible while transforming the original structures. Knowing what survives that transformation helps distinguish elemental analysis from chemical speciation.

## Define the fraction before preparing the sample

A clear liquid can contain particles too small to see, particularly in nanoparticle studies or during slow dissolution of inorganic fillers. For an operationally defined dissolved fraction, the order of preparation matters. EPA Method 200.7 specifies filtration through 0.45 μm before acidification. That pore size defines a procedure; sufficiently small particles may still pass. Acid added before filtration can dissolve material that would otherwise have remained particulate. Recording pore size, filtration order, collection time and liquid volume therefore ensures that different groups represent comparable fractions rather than superficially similar bottles.

Measuring particles together with the liquid requires an appropriate extraction or digestion. A method-defined total recoverable result does not automatically include every element trapped in a resistant crystal. Polymers, tissues, ceramics and silicate-containing solids present different decomposition problems. Preparation should match the matrix and target elements and be supported by suitable recovery evidence or reference materials. A clear final solution shows that visible particles have decreased, but complete elemental release requires its own validation. For a composition study, this determines whether the result describes the total amount or an operationally extractable fraction.

The worked example starts with 0.2500 g of a dry, low-calcium composite. The calculation assumes complete calcium release into a digest brought to a final volume of 50.00 mL. Making to volume means completing dissolution and transfer, then adjusting the total solution volume; it does not mean simply adding 50 mL of liquid. A portion of that digest is diluted a further tenfold before introduction. The dry specimen mass, digest volume and additional dilution factor are retained separately. Together they convert an instrumental result in mg/L into a material result in mg/kg. Using a wet specimen would change the denominator and require a corresponding wet-mass or as-received definition.

For trace analysis, containers and reagents contribute to the sample history. Water, acids, filters, tubes and tools can introduce target elements, while concentrated solutions can leave residues in the introduction system. A method blank follows the relevant preparation steps and reveals these contributions. A calibration blank establishes the zero end of the calibration under its chosen acid matrix. Spectral background subtraction, calibration intercept and method blank are therefore different concepts. They are not three interchangeable corrections to subtract automatically. An elevated method blank should prompt investigation and review of affected samples; a single contaminated blank is not a universal correction for the entire batch.

Dilution can improve comparability by reducing salt content, acidity or viscosity, thereby making aerosol generation and transport more similar to the standards. It also lowers the target concentration, making blank variability more consequential. A preliminary appropriately diluted portion can help locate the useful range, after which the selected conditions are checked against calibration coverage and matrix behaviour. The final calculation uses every actual volume and dilution step. A remembered statement such as “about tenfold” cannot replace those quantities when returning from a solution measurement to the original material.

## A calcium line also has neighbours

A spectrometer directs different wavelengths toward different detection positions, but an observed line has a finite width. Particle motion, the emitting environment and instrumental resolution all contribute to the recorded shape. Even a narrow transition occupies a region of the measured spectrum. Nearby lines can overlap like two voices heard through a wall: a higher combined peak may reflect more analyte, more interference, or both. Line selection therefore considers sensitivity together with neighbouring elements, background, matrix concentration and the instrument's actual resolving capability.

This chapter places the target at the Ca II air wavelength of 317.9332 nm. The NIST calcium table also lists, for example, Ca II at 393.36614 nm and Ca I at 422.6727 nm. Such wavelength facts help locate transitions; tabulated relative intensities arise under particular source conditions and do not replace a concentration calibration on the instrument being used. The neighbouring peak in the teaching spectrum is explicitly constructed and is not assigned to a real iron, nickel or other transition. Its adjustable position isolates the consequences of overlap without inventing a line identification.

![Constructed spectra and executed fits. The target uses the NIST Ca II air wavelength 317.9332 nm; the second peak is constructed, with 0.018 nm separation and common FWHM 0.014 nm. Noise SD is 20 a.u.; the residual band spans ±40 a.u. Panel D uses the condition number of two normalized peak columns after constant/linear-background projection.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/9e35217b6ff8f5d0cd1107c8.svg?v=9e35217b6ff8)

Figure 2Constructed spectra and executed fits. The target uses the NIST Ca II air wavelength 317.9332 nm; the second peak is constructed, with 0.018 nm separation and common FWHM 0.014 nm. Noise SD is 20 a.u.; the residual band spans ±40 a.u. Panel D uses the condition number of two normalized peak columns after constant/linear-background projection.

A spectral window also contains background. One approach estimates it from nearby regions free of lines, then extracts the analyte contribution above that estimate. The background regions themselves need inspection. If another emission line is mistakenly used as a background point, the subtraction can be too large and the concentration too low. Direct overlap often raises the apparent signal, whereas contaminated background positions can lower it. Bias direction alone therefore does not identify the cause. Inspecting the full window, comparing an alternative usable line and checking dilution consistency provide complementary evidence.

$$
y_i=A\,g_i+B\,h_i+b_0+b_1x_i+\varepsilon_i
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | Wavelength-sample index, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/a51d7c6c42d3bb0b61f865ba.svg) | Observed signal at point i, a.u. (arbitrary but consistent signal units) |
| ![Formula](https://ml-biomat.com/static/agent-math/f12c13576bb625453e573142.svg) | Target and interfering peak heights, a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/4c96cf679f9702a712ef0a78.svg) | Two profiles at specified positions and widths, normalized to unit peak height, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/1786b0ad5e438341adfba90f.svg) | Linear background at the target centre, a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/86ef2a91a3da50f97dc73bcd.svg) | Background slope, a.u./nm |
| ![Formula](https://ml-biomat.com/static/agent-math/10c16af3229388fdcbca3de7.svg) | Wavelength offset from the target centre, nm |
| ![Formula](https://ml-biomat.com/static/agent-math/df6c5ac19bbf29886eee1c95.svg) | Random signal error at point i, a.u. |

Within linear detector response, light contributions add. Here A=7680, B=4608, b₀=250 and b₁=800. At the target centre x=0, g=1 and the neighbouring tail h is about 0.01022, giving a mean near 7977.1 a.u. Positions and widths are fixed for least squares. Identical profiles determine A+B alone; separating them requires independent information.

The model represents the observation as a target peak, an interfering peak, a slowly varying background and random noise. Each peak shape has unit height at its centre, so its coefficient is a peak height in signal units. Other methods can use areas or different profiles, provided standards and samples are treated consistently. Here the positions and widths are fixed while the fit estimates contributions. When the shapes are almost identical, increasing one coefficient and decreasing the other can leave the total fitted curve almost unchanged. A small residual alone therefore does not establish accurate individual peak estimates.

The interactive experiment reports a condition number to expose this sensitivity. It first removes the constant and linear background directions from both profiles, then normalizes the remaining profiles to equal length before assessing their similarity. Values near one indicate readily distinguishable directions; close overlap can greatly amplify small noise contributions. Exactly coincident profiles supply only their combined contribution. Resolving the separate amounts then requires another line, improved effective resolution or genuinely independent information. The interface makes this loss visible instead of reporting a precise concentration for every possible overlap.

Observation geometry also affects the available signal. Axial viewing looks along the plasma and often collects light over a longer path, which can increase sensitivity while also collecting more background or matrix effects. Radial viewing observes from the side, sampling a different path and region that may suit demanding matrices. These are geometries for observing the source, not two unrelated kinds of plasma. At sufficiently high concentration, self-absorption can also bend the response: emitted light is absorbed again before leaving the source. Line choice, viewing geometry and dilution should together place standards and samples within a verified response range.

## Return from a signal to one gram of material

A calibration gives the signal a scale. The example uses calcium levels of 0, 0.25, 0.50, 1.00 and 2.00 mg/L, with three constructed injections at each level, and fits a straight line with an intercept. In laboratory work the standards need traceable concentrations, appropriate preparation volumes and a suitable acid matrix. Standards made from one stock share that stock's possible concentration error. Repeated injections reveal short-term scatter but do not expose a common preparation bias. A check solution from an independent source can therefore contribute information that additional injections from the same bottle cannot.

$$
S=a c+b,\qquad \widehat c=\frac{S_{\mathrm{sample}}-b}{a}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4d93e1f4798eafa4154488df.svg) | Net standard line signal, a.u.; spectral background has been handled consistently |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | Standard elemental concentration, mg/L |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | Calibration slope, a.u. per mg/L |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | Calibration intercept, a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/d5e0d97dd9bcf99758f72c2f.svg) | Sample signal processed like the standards, a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/70e13ece2487a9b7956f0a74.svg) | Estimated concentration in the introduced solution, mg/L; the hat marks an estimate |

Within a linear range and comparable response conditions, subtract the origin and convert units using the slope. Ideal a=12000, b=150 and sample signal 9750 give 0.800 mg/L. Constructed observations fit a≈12002.666 and b≈142.092, recovering 0.8005197 mg/L from three unknown readings. A method blank diagnoses preparation contamination; it is not a second subtraction of the same intercept.

The slope describes how much signal increases for each additional mg/L; the intercept represents the zero-concentration response under the calibration's processing conditions. Subtracting the intercept aligns the origin, and dividing by the slope converts signal units to concentration units. The executed example gives a slope of approximately 12002.67 a.u. per mg/L and an intercept of 142.09 a.u. Three unknown injections give a mean back-calculated concentration of about 0.80052 mg/L. These are explicitly constructed observations with fixed random noise, which explains why the recovered result differs slightly from the specified value of 0.80000.

![Constructed five-level calibration and low-calcium composite example, with three observations at each level and fixed random noise. The three unknown injections give about 0.80052 mg/L. Panel C assumes complete calcium release into 50.00 mL digest from 0.2500 g dry material, followed by tenfold dilution, giving about 1601.04 mg/kg.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/971406515042a9ebfdcf636e.svg?v=971406515042)

Figure 3Constructed five-level calibration and low-calcium composite example, with three observations at each level and fixed random noise. The three unknown injections give about 0.80052 mg/L. Panel C assumes complete calcium release into 50.00 mL digest from 0.2500 g dry material, followed by tenfold dilution, giving about 1601.04 mg/kg.

Residuals deserve attention after fitting. A residual is the observation minus the fitted value. A systematic curved pattern suggests that a straight line is missing structure. Increasing scatter at high concentration raises questions about concentration-dependent uncertainty and suitable weighting. A high correlation can coexist with a practically important error near the low end, because high-concentration points dominate the overall range. Plotting all fifteen observations and their residuals makes calibration a diagnosable measurement relationship rather than a single impressive statistic. An unknown should also fall within the validated range; an above-range solution is normally diluted and measured again.

$$
w=\frac{\widehat c\,D\,V}{m_s}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/5f85a26e5089def254fee2b9.svg) | Element content of the original dry material, mg/kg |
| ![Formula](https://ml-biomat.com/static/agent-math/70e13ece2487a9b7956f0a74.svg) | Back-calculated concentration in the final introduced solution, mg/L |
| ![Formula](https://ml-biomat.com/static/agent-math/5914524b1d3db63c66998b75.svg) | Total dilution factor from digest to introduced solution, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/bef27a67f1f86637c8224c0d.svg) | Final volume of the complete original digest, L |
| ![Formula](https://ml-biomat.com/static/agent-math/e9ba2f332f9416cc47936a32.svg) | Original dry specimen mass represented by that digest, kg |

Assuming complete elemental release and transfer, concentration times volume gives elemental mass, which is divided by specimen mass. The example gives 0.800×10×0.05000/0.0002500=1600 mg/kg=0.16% by mass. The noisy calibration example gives about 1601.04 mg/kg. Extraction measurements use their own collected volumes and sampling account and describe the corresponding released amount.

In the ideal example, 0.800 mg/L belongs to the final introduced solution. Multiplying by ten recovers 8.00 mg/L in the original digest. Multiplying by 0.05000 L gives 0.400 mg of calcium in the complete digest, and dividing by 0.0002500 kg of material gives 1600 mg/kg, or 0.16% by mass. That composition fits the low-calcium composite example; it is not presented as typical of a pure calcium phosphate solid. Substituting the executed concentration gives about 1601.04 mg/kg. The intermediate elemental mass is especially useful for detecting thousandfold errors from mixing millilitres with litres or grams with kilograms.

For an extraction study the same arithmetic answers a different question. A completely collected 20.0 mL extract at 0.800 mg/L contains 0.0160 mg of calcium. If it came from 0.2500 g of material, that collection represents 0.0640 mg/g released under the specified conditions. During repeated sampling with replacement, earlier removed calcium must also enter the cumulative account. Multiplying a final concentration by the current vessel volume misses what has already left in earlier aliquots. Concentration, collection time, withdrawn volume and replacement history together distinguish cumulative release, release rate and remaining material composition.

## How internal standards and additions follow a changing response

The matrix comprises the other components of a sample solution. Acidity, salt loading, viscosity and surface tension can affect nebulization, droplet selection and transport. Composition within the plasma can also affect excitation and ionization. Suppose 0.800 mg/L calcium gives a background-corrected signal of 9600 a.u. in standards, but a sample reduces delivery to 80%. The same calcium then produces 7680 a.u. Applying the original external-calibration slope of 12000 gives 0.640 mg/L. Repeated injections may reproduce that biased value very closely. Repeatability and accuracy thus require different experimental checks.

An internal standard adds the same concentration of another element to standards, blanks and samples. If its reference signal is 5000 a.u. and it falls to 4000 a.u. in the sample, both channels have fallen to 80%, so their ratio cancels the shared factor. The selected element should have suitably low native abundance, or that contribution must be handled explicitly. Its line must be free of relevant interference, and its response must be shown to follow the analyte sufficiently well in the actual matrices. Calling something an internal standard does not make its behaviour automatically suitable.

$$
c_{\mathrm{IS}}=\frac{S_A}{a}\frac{S_{I,\mathrm{ref}}}{S_I}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a0c96901b8b2ce501d0ff987.svg) | Internally corrected concentration in the ideal shared-response model, mg/L |
| ![Formula](https://ml-biomat.com/static/agent-math/fbfc0f565ed61fb4e844ec2b.svg) | Analyte signal after the appropriate background and intercept correction, a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | Analyte calibration slope under reference conditions, a.u. per mg/L |
| ![Formula](https://ml-biomat.com/static/agent-math/39e7b1a43cfe84d51c42ad59.svg) | Net internal-standard signal in the sample, a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/562b42e43fdbcfd6045d461a.svg) | Net internal-standard signal under reference conditions at the same added concentration, a.u. |

If analyte and internal standard share a multiplicative transport factor, the ratio removes it. Here 7680/12000×5000/4000=0.800 mg/L versus 0.640 mg/L externally. This ideal illustration assumes appropriate zero correction; actual methods can calibrate the signal ratio directly. Analyte-specific interference and preparation losses require separate checks.

![Exactly specified teaching models. Shared response reduction to 80% gives 0.640 mg/L externally and 0.800 mg/L after ideal internal correction. Standard additions keep final volume and matrix constant. The final four checks have an extra 8% analyte-specific suppression, leaving 92% after internal correction; post-digestion spikes assess subsequent response.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/4f48c865fb818e19fc4a8b97.svg?v=4f48c865fb81)

Figure 4Exactly specified teaching models. Shared response reduction to 80% gives 0.640 mg/L externally and 0.800 mg/L after ideal internal correction. Standard additions keep final volume and matrix constant. The final four checks have an extra 8% analyte-specific suppression, leaving 92% after internal correction; post-digestion spikes assess subsequent response.

In the first twelve constructed check solutions, the only change is shared response loss, which the ratio corrects. The final four introduce an additional 8% analyte-specific suppression; the internal standard continues to follow the common change, so the corrected result remains at 92% of the true value. This identifies what the correction measures: a shared multiplicative factor. Additional optical emission, incomplete elemental release and prior losses to container walls need their own investigation. Alternative lines, dilution comparisons and preparation recovery evidence help separate these causes rather than applying one correction indiscriminately.

Standard additions compare solutions made from equal aliquots of the same unknown. Different known amounts of analyte are added, and every solution is brought to the same final volume. The original sample contribution and matrix are thereby kept approximately constant while added concentration changes. Extrapolating signal against added concentration to zero signal estimates the native contribution in that final volume. If the aliquot was diluted during this preparation, the corresponding final-volume-to-aliquot-volume factor is applied once to recover the original solution concentration. The intercept should not be silently relabelled as the concentration in the initial digest.

$$
S=q(c_x+c_{\mathrm{add}}),\qquad c_x=\frac{\beta}{q},\qquad c_{\mathrm{add},0}=-\frac{\beta}{q}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4d93e1f4798eafa4154488df.svg) | Standard-addition signal after appropriate background correction, a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/9dc96195196376263c1f2c83.svg) | Response slope in the constant sample matrix, a.u. per mg/L |
| ![Formula](https://ml-biomat.com/static/agent-math/9c54bbce30583a2aa825733e.svg) | Native sample contribution in each equal final volume, mg/L |
| ![Formula](https://ml-biomat.com/static/agent-math/3f452a9afb83108541dff1a7.svg) | Known added concentration in each final volume, mg/L |
| ![Formula](https://ml-biomat.com/static/agent-math/f27acf6959fc15846a7239da.svg) | Signal-axis intercept of the additions fit, a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/edbf9de74fec745b1752934a.svg) | Added-concentration-axis intercept at zero fitted signal, mg/L |

Equal sample aliquots, equal final volumes and linear shared matrix response give the same response factor for native and added analyte. With q=9600 and β=7680, cx=0.800 mg/L and the horizontal intercept is −0.800 mg/L. This cx belongs to the final mixture; recover the initial solution using the final-volume-to-aliquot-volume factor once. Additive spectral contributions bias β.

The illustration assigns a native contribution of 0.800 mg/L in each final solution and additions of 0, 0.400, 0.800 and 1.200 mg/L. Matrix suppression reduces the slope to 9600 a.u. per mg/L, with an intercept of 7680 a.u. Dividing intercept by slope still gives 0.800, so the horizontal intercept is −0.800 mg/L. This works because the same response factor multiplies native and added analyte. An extra line or uncorrected background offset changes the intercept without changing the addition slope in the same way. Such an additive contribution is then misinterpreted as native analyte, making spectral inspection essential before using additions.

A spike recovery check expresses the comparison directly. On a common final-volume basis, adding 0.500 mg/L to a native 0.800 mg/L should increase the result by 0.500. If external-calibration results rise from 0.640 to 1.040, the observed increase is 0.400 and recovery is 80%. A soluble spike added after digestion tests subsequent response, but it has not experienced release from the original solid. Assessment of the complete preparation needs suitable evidence at that level. Comparing these checks helps turn “20% low” into a question about spectra, introduction, matrix or preparation.

$$
R=\frac{c_{\mathrm{spiked}}-c_{\mathrm{native}}}{c_{\mathrm{added}}}\times100\%
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/085f4d77675f3cb7323d94fe.svg) | Spike recovery, % |
| ![Formula](https://ml-biomat.com/static/agent-math/3aa442cea385f1c181f3e880.svg) | Measured spiked-sample concentration, mg/L |
| ![Formula](https://ml-biomat.com/static/agent-math/e6504e8fba3cf3faca91399c.svg) | Measured unspiked concentration on the same final-volume basis, mg/L |
| ![Formula](https://ml-biomat.com/static/agent-math/e077c72fdd39aab03ec09b0c.svg) | Added concentration on that same final-volume basis, mg/L |

The spiked-minus-unspiked increment should equal the added amount. External results of 1.040 and 0.640 mg/L with a 0.500 mg/L addition give 80%; correct shared-response correction restores a 0.500 increment and 100%. A post-digestion addition assesses subsequent steps; release from the original material requires suitable separate evidence.

## Small signals, reference materials and interpretable uncertainty

Near zero concentration the signal does not become perfectly still. Detector variability, background estimation and sample introduction all produce scatter. Estimating that scatter is an initial step toward assessing a small signal. The example constructs ten calibration-blank readings, calculates their sample standard deviation in signal units, and uses the calibration slope to express the scale in concentration units. Replacing every negative back-calculated concentration with zero would artificially compress the distribution. Retaining the original low-level observations for noise estimation is a different task from deciding how results below a reporting threshold are labelled in a final table.

$$
s_B=\sqrt{\frac{\sum_{j=1}^{n}(B_j-\overline B)^2}{n-1}},\qquad c_{3s}=\frac{3s_B}{a},\qquad c_{10s}=\frac{10s_B}{a}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1f990247057bfe614e52c27c.svg) | Calibration-blank signal for observation j, a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/23c2accd18c3dd312fe92883.svg) | Arithmetic mean of those blank signals, a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/a685ea95c60540ff028f8ac9.svg) | Observation index and count, dimensionless; here n=10 |
| ![Formula](https://ml-biomat.com/static/agent-math/284686c1a37c7859ac406591.svg) | Sample standard deviation of blank signals, a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | Calibration slope, a.u. per mg/L |
| ![Formula](https://ml-biomat.com/static/agent-math/65d71ecfdd9bf632552deabc.svg) | Concentration scales corresponding to three and ten signal standard deviations, mg/L |

Squared deviations measure scatter. The unsquared deviations from the sample mean sum to zero, leaving n−1 independent pieces of information, so the denominator is n−1. With sB≈11.0629 and a≈12002.666, the scales are 0.00276511 and 0.00921703 mg/L. This is a simplified instrumental-noise conversion. Method detection and quantification limits also need full preparation, multiple batches and low-level bias/precision verification.

The executed blank standard deviation is about 11.063 a.u. Dividing three times that value by the slope gives approximately 0.002765 mg/L; ten times gives approximately 0.009217 mg/L. These describe concentration scales in the simplified instrumental-noise example. Method-level detection capability also incorporates preparation contamination, low-level recovery and variation between batches and days. The revised EPA method-detection-limit procedure includes both spiked samples and method blanks across multiple batches. A quantification limit also needs low-level bias and precision verification. Dilution raises the corresponding original-sample threshold; the present material conversion factor is 2000 L/kg, so a solution-side number cannot be quoted unchanged for the solid.

Certified reference materials provide a different comparison. NIST SRM 1643f is a trace-element water reference material. The chapter replots four actual certified mass concentrations: calcium 29.430 mg/L, magnesium 7.454 mg/L, strontium 0.314 mg/L and zinc 0.0744 mg/L. These span different ranges, so a single preparation may not place every element in a suitable measurement interval. Calcium requires dilution for the example's 0–2 mg/L calibration, while a dilute element subjected to the same factor could approach the low end. A multielement measurement plan therefore checks the resulting concentrations element by element.

![Original plot of the mass-concentration column in the NIST SRM 1643f certificate, converted from μg/L to mg/L by division by 1000. Error bars are certified expanded uncertainties with approximately 95% coverage and the individual factors shown at right, not replicate measurements acquired here. The left axis is logarithmic; the right shows each expanded uncertainty relative to its concentration.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/ee43faae37ac4ba58f6eb08a.svg?v=ee43faae37ac)

Figure 5Original plot of the mass-concentration column in the NIST SRM 1643f certificate, converted from μg/L to mg/L by division by 1000. Error bars are certified expanded uncertainties with approximately 95% coverage and the individual factors shown at right, not replicate measurements acquired here. The left axis is logarithmic; the right shows each expanded uncertainty relative to its concentration.

The four expanded uncertainties are 0.330, 0.060, 0.019 and 0.0017 mg/L. Their coverage factors are respectively 2.1, 2.0, 2.2 and 2.1, with approximately 95% coverage. These intervals summarize the certification process and its relevant uncertainty components. They are not standard deviations from repeated injections performed for this chapter. The second panel divides each expanded uncertainty by its own concentration, revealing a relative value of about 6.05% for strontium. This shows both the actual concentration range and the relative width of each certified interval without imposing a single percentage on every element.

The certificate separately reports mass fraction and mass concentration. Their denominators are kilograms of solution and litres of solution, connected through solution density. Here the mass-concentration column is used, and μg/L is divided by 1000 to obtain mg/L. The role of a reference material should also match the question: an aqueous material can assess solution measurement and dilution, while complete digestion of a solid requires evidence suited to that matrix and elemental binding. Reference materials, independent checks, method blanks, preparation duplicates and spikes each examine a different part of the measurement chain.

Long sequences also need evidence about time. Check solutions placed through the sequence help distinguish a sample change from instrumental drift. Rinse blanks after concentrated samples reveal carryover. When a check shifts, inspect the affected time interval, lines, internal-standard response and introduction conditions, then reassess the relevant samples. This connects the reported concentration to an experimentally defined sequence. The useful result is not simply a string of decimal places but an amount whose preparation, calibration and quality controls support its interpretation.

## Change resolution, then run the complete analysis

The interactive experiment fixes the true concentration at 0.800 mg/L and lets you change line separation, observed full width at half maximum, interfering-peak strength and the shared matrix response. Full width at half maximum is the distance between the two positions at half the peak height. Larger values mean a broader line. First reduce separation while keeping other settings fixed, watching the spectrum, joint fit, condition number and concentration estimates together. Then restore sufficient separation and reduce only the matrix response from one to 0.8. Comparing external and internally corrected results separates overlap from common transport loss.

## Interactive experiment: does resolving the lines guarantee the concentration?

The known calcium concentration stays at 0.800 mg/L and the target air wavelength at 317.9332 nm. Move the neighbouring line, then change the width and compare the spectrum, residuals and concentration estimates. Next change only the shared matrix response to see external and internal-standard estimates separate. The lower-right error bars show twice the model standard error. Every setting uses the same fixed noise realization.

[Figure: Linked ICP spectrum, fit residuals and three concentration readings](https://ml-biomat.com/tutorials/experimental-methods/s08/en/#S08-plot)

| Reading method | Concentration / mg L⁻¹ | What it handles under this model |
| --- | --- | --- |
| Read the target centre directly |  | The known background is removed; the neighbouring line still contributes. |
| Joint peak fit with external calibration |  | Separates the specified profiles; matrix response still changes the result. |
| Joint fit with internal-standard correction |  | Also cancels the response factor shared exactly by both channels. |

The two profiles are Gaussian, with known centres and widths. Background is linear and independent point noise has a standard deviation of 20 a.u. The condition number describes the two normalized profiles after removing constant and linear background components. At exact coincidence, the total curve can still be fitted, but calcium cannot be separated within this window; individual concentrations are then withheld. The internal-standard channel tracks the shared factor exactly in this model; experiments need to establish how closely the two responses track.

The displayed uncertainty scale assumes that both positions, widths and profiles are correctly specified and that the independent point noise has a standard deviation of 20 a.u. Twice the model standard error helps compare these controlled settings; it does not include wrong line assignments, an inappropriate background model or preparation losses. At exact coincidence the total curve can still fit well, but individual contributions are unidentified, so separate concentrations are withheld. Trying that setting makes the difference between a visually good fit and sufficient information tangible.

The complete Python example constructs calibration observations and spectra, fits the contributions, examines residuals, recovers the unknown concentration and returns it to a specimen mass basis. It also produces the standard-addition and quality-control figures and reads the bundled four-element certificate table. Fixed random numbers make the generated observations reproducible; changing language changes labels rather than numerical results. Output tables retain observations, fitted values and residuals for direct inspection. Certified facts and constructed observations remain separately identified throughout the example.

### Complete example: From spectra and calibration to material content

Runs offline and exports five localized figures, calibration/spectrum/check/certificate tables and summary.json. Spectra, calibration and QC are specified teaching constructions; the four-element table contains NIST certified mass concentrations.

```
"""ICP-OES: reproducible teaching models and actual NIST certificate values.

All spectra, calibration observations and QC sequences are constructed examples.
The four SRM rows are certified numerical facts, not measurements made here.
Run: python main.py --output results --language en
"""
from pathlib import Path
import argparse
import csv
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Ellipse, FancyArrowPatch

BLUE, GREEN, ORANGE, PURPLE = '#236d96', '#18877d', '#d57b39', '#8863a4'


def fixed_noise(n, seed=804):
    """Specified LCG + Box-Muller, shared exactly with the browser laboratory."""
    out = []
    while len(out) < n:
        seed = (1664525 * seed + 1013904223) & 0xffffffff
        u = (seed + .5) / 4294967296
        seed = (1664525 * seed + 1013904223) & 0xffffffff
        v = (seed + .5) / 4294967296
        out.extend([np.sqrt(-2*np.log(u))*np.cos(2*np.pi*v),
                    np.sqrt(-2*np.log(u))*np.sin(2*np.pi*v)])
    return np.array(out[:n])


def spectral_model(separation=.018, width=.014, interference=.6, matrix=.8):
    x = np.linspace(-.06, .06, 241)
    sigma = width / np.sqrt(8*np.log(2))
    g = np.exp(-.5*(x/sigma)**2)
    h = np.exp(-.5*((x-separation)/sigma)**2)
    baseline = 250 + 800*x
    y = baseline + matrix*12000*.8*(g+interference*h) + 20*fixed_noise(len(x))
    bg = np.column_stack([np.ones(len(x)), x])
    gp = g-bg@np.linalg.lstsq(bg, g, rcond=None)[0]
    hp = h-bg@np.linalg.lstsq(bg, h, rcond=None)[0]
    rho = float(gp@hp/np.sqrt((gp@gp)*(hp@hp)))
    identifiable = abs(rho) < 1-1e-12
    condition = np.sqrt((1+abs(rho))/(1-abs(rho))) if identifiable else None
    design = np.column_stack([g, h, np.ones(len(x)), x])
    if identifiable:
        coef = np.linalg.lstsq(design, y, rcond=None)[0]
        se = 20*np.sqrt(np.linalg.inv(design.T@design)[0, 0])/(12000*matrix)
        external, corrected = coef[0]/12000, coef[0]/(12000*matrix)
    else:
        combined = np.column_stack([g, np.ones(len(x)), x])
        c = np.linalg.lstsq(combined, y, rcond=None)[0]
        coef = np.array([c[0], 0, c[1], c[2]])
        external = corrected = se = None
    fit = design@coef
    return {'x':x, 'y':y, 'fit':fit, 'g':g, 'h':h, 'baseline':baseline,
            'coef':coef, 'identifiable':identifiable,
            'condition':float(condition) if identifiable else None,
            'external_mg_L':float(external) if identifiable else None,
            'corrected_mg_L':float(corrected) if identifiable else None,
            'standard_error_mg_L':float(se) if identifiable else None,
            'residual_rms':float(np.sqrt(np.mean((y-fit)**2))),
            'center_naive_mg_L':float((y[120]-baseline[120])/12000)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=Path('results'))
    parser.add_argument('--language', choices=['zh','en'], default='en')
    args = parser.parse_args()
    out, lang = args.output, args.language
    out.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],
                         'font.size':11, 'axes.spines.top':False,
                         'axes.spines.right':False, 'svg.fonttype':'none',
                         'axes.labelcolor':'#293c49','text.color':'#293c49',
                         'axes.titleweight':'bold','figure.facecolor':'#fffdf9'})
    def t(zh,en): return zh if lang=='zh' else en
    def save(fig,name):
        fig.savefig(out/f'{name}-{lang}.svg', bbox_inches='tight')
        fig.savefig(out/f'{name}-{lang}.png', dpi=150, bbox_inches='tight')
        plt.close(fig)
    def csvsave(name, header, rows):
        with (out/name).open('w',encoding='utf-8',newline='') as f:
            w=csv.writer(f); w.writerow(header); w.writerows(rows)

    # 1: original historical/mechanistic drawing, not a copied historical apparatus.
    fig=plt.figure(figsize=(14,10),layout='constrained')
    gs=fig.add_gridspec(2,2,height_ratios=[1,1.7])
    ax=fig.add_subplot(gs[0,0]); ax.set(xlim=(0,10),ylim=(0,5)); ax.axis('off')
    ax.set_title(t('A  从火焰颜色到可分辨谱线','A  From flame colour to resolved lines'),loc='left')
    ax.add_patch(Polygon([[.8,1],[1.3,3.3],[1.8,1]],color=ORANGE,alpha=.8))
    ax.add_patch(Rectangle((.8,.6),1,.4,color='#8a949d'))
    ax.add_patch(Rectangle((3,.7),.15,1.18,color='#293c49'))
    ax.add_patch(Rectangle((3,2.12),.15,1.28,color='#293c49'))
    ax.add_patch(Polygon([[5,1],[5.7,3.2],[6.4,1]],facecolor='#cae8ec',edgecolor=BLUE))
    ax.plot([1.4,5.5],[2,2],color=ORANGE,lw=2)
    for yy,col in [(1.2,PURPLE),(2,GREEN),(2.8,ORANGE)]:
        ax.plot([5.5,8.6],[2,yy],color=col,lw=2); ax.plot([8.7,8.7],[yy-.2,yy+.2],color=col,lw=3)
    ax.text(.4,.1,t('火焰','Flame')); ax.text(2.5,.1,t('狭缝','Slit')); ax.text(5,.1,t('棱镜','Prism'))
    ax.text(.3,4,t('1860：基尔霍夫与本生的光谱分析','1860: Kirchhoff and Bunsen — spectral analysis'),fontsize=11)
    ax=fig.add_subplot(gs[0,1]); ax.set(xlim=(0,10),ylim=(0,5)); ax.axis('off')
    ax.set_title(t('B  1964年的问题：同样的钙，为什么变暗？','B  The 1964 question: why does calcium look dimmer?'),loc='left')
    for xpos,height,label in [(2,2.1,t('钙溶液','Calcium solution')),(6,1.1,t('钙 + 磷 / 铝','Calcium + P / Al'))]:
        ax.add_patch(Rectangle((xpos,.8),1,height,color=ORANGE,alpha=.7))
        ax.text(xpos+.5,.4,label,ha='center',fontsize=10)
    ax.text(.3,4,t('火焰中的化学干扰 → 探索高温感应等离子体','Chemical interference in flames → induction plasma'),fontsize=11)
    ax.text(.3,3.2,t('概念图；柱高不是历史测量数据','Conceptual illustration; bar heights are not historical data'),fontsize=10,color='#687782')
    ax=fig.add_subplot(gs[1,:]); ax.set(xlim=(0,16),ylim=(0,6)); ax.axis('off')
    ax.set_title(t('C  一滴样品怎样成为元素的光','C  How a droplet becomes elemental light'),loc='left')
    ax.add_patch(Rectangle((.35,1.4),1.15,1.4,facecolor='#ecf5f7',edgecolor=BLUE,lw=1.5))
    ax.add_patch(Rectangle((.38,1.43),1.09,.7,facecolor='#99d0dc',alpha=.7))
    ax.plot([.92,.92,2.0,2.0],[1.7,3.2,3.2,2.9],color=BLUE,lw=2)
    ax.text(.9,1.05,t('样品瓶','Sample'),ha='center')
    ax.add_patch(Polygon([[1.85,2.6],[2.7,2.8],[1.85,3]],facecolor='#bedae6',edgecolor=BLUE))
    ax.text(2.2,3.65,t('雾化器','Nebulizer'),ha='center')
    ax.annotate(t('氩气','Argon'),xy=(1.9,2.65),xytext=(1.6,2.05),arrowprops={'arrowstyle':'->','color':GREEN},fontsize=10)
    ax.add_patch(Polygon([[2.8,1.9],[3.4,1.6],[5.8,1.6],[6.3,2.2],[6.3,3.5],[3.2,3.5],[2.8,3.1]],facecolor='#eef5f7',edgecolor=BLUE,lw=1.5))
    ax.text(4.5,3.85,t('雾室：筛去大液滴','Spray chamber: remove large drops'),ha='center',fontsize=11)
    ax.scatter([3,3.3,3.5,3.8,4.1,4.5,5,5.5,5.9],[2.8,2.7,2.95,2.8,2.9,2.82,2.86,2.87,2.9],s=[30,20,12,8,6,5,4,4,3],color=BLUE)
    ax.scatter([3.4,4.2,4.6],[2.3,2.05,1.85],s=[45,70,55],color=BLUE,alpha=.65)
    ax.plot([4.6,4.6],[1.6,.95],color=BLUE,lw=2)
    ax.annotate('',xy=(4.6,.65),xytext=(4.6,1.3),arrowprops={'arrowstyle':'->','color':BLUE})
    ax.text(4.65,.35,t('大液滴与废液','Large drops / drain'),ha='center',fontsize=10)
    ax.plot([6.3,7.5],[2.9,2.9],color=BLUE,lw=3)
    for height,start,end in [(1.8,7.4,11.1),(1.25,7.6,10.5),(.45,7.4,10.0)]:
        ax.plot([start,end],[2.9-height/2]*2,color='#8dafbf',lw=2)
        ax.plot([start,end],[2.9+height/2]*2,color='#8dafbf',lw=2)
    for xcoil in [8.3,8.65,9,9.35]:
        ax.add_patch(Ellipse((xcoil,2.9),.28,2.1,facecolor='none',edgecolor=ORANGE,lw=2.8))
    ax.add_patch(Ellipse((10.5,2.9),2.4,1.05,facecolor=PURPLE,alpha=.22))
    ax.add_patch(Ellipse((10.3,2.9),1.8,.6,facecolor=ORANGE,alpha=.24))
    ax.annotate('',xy=(10.7,2.9),xytext=(6.6,2.9),arrowprops={'arrowstyle':'->','color':BLUE,'lw':1.8})
    ax.annotate('',xy=(9.8,3.62),xytext=(7.5,3.62),arrowprops={'arrowstyle':'->','color':GREEN,'lw':1.5})
    ax.text(7.7,4.25,t('石英同心炬管','Concentric quartz torch'),ha='center',fontsize=11)
    ax.text(8.8,1.35,t('外绕射频线圈','External RF coil'),ha='center',color=ORANGE,fontsize=11)
    ax.text(8.9,.85,t('中心：样品气溶胶','Centre: sample aerosol'),ha='center',fontsize=10)
    ax.text(10.8,1.65,t('氩等离子体','Argon plasma'),ha='center',fontsize=11)
    ax.annotate('',xy=(13.5,2.9),xytext=(11.7,2.9),arrowprops={'arrowstyle':'->','color':PURPLE,'lw':2})
    ax.text(12.8,2.45,t('轴向看光','Axial light'),ha='center',color=PURPLE,fontsize=10)
    ax.annotate('',xy=(10.8,4.75),xytext=(10.8,3.45),arrowprops={'arrowstyle':'->','color':GREEN,'lw':2})
    ax.text(11.05,4.05,t('径向看光','Radial light'),color=GREEN,fontsize=10)
    ax.plot([10.8,13.4],[4.75,4.75],color=GREEN,lw=1.5,ls='--')
    ax.plot([13.5,13.5],[2.9,4.75],color=PURPLE,lw=1.5,ls='--')
    ax.add_patch(Rectangle((13.5,4.15),2.2,1.2,facecolor='#f0edf5',edgecolor=PURPLE))
    ax.text(14.6,4.75,t('分光光学系统\n与检测器','Spectrometer\nand detector'),ha='center',va='center',fontsize=11)
    ax.text(.3,5.25,t('原理剖面示意；两条光路表示可选择的观察方向','Functional cross-section; two light paths represent alternative viewing directions'),fontsize=11)
    ax.text(12.5,.45,t('去溶剂 → 原子化 → 激发 / 电离','Desolvation → atoms → excitation / ionization'),ha='center',fontsize=10)
    save(fig,'light-path')

    # 2: spectral overlap and identifiability. Line centre is NIST air wavelength.
    sp=spectral_model()
    fig,axs=plt.subplots(2,2,figsize=(13,8.5),layout='constrained')
    ax=axs[0,0]; xx=317.9332+sp['x']
    ax.plot(xx,sp['y'],color='#86939c',lw=1,label=t('构造观测','Constructed observations'))
    ax.plot(xx,sp['fit'],color=BLUE,lw=2,label=t('联合拟合','Joint fit'))
    ax.set(title=t('A  两条谱线与背景','A  Two lines and a background'),ylabel=t('信号 / a.u.','Signal / a.u.'))
    ax.legend(fontsize=9);ax.ticklabel_format(useOffset=False,axis='x')
    ax=axs[1,0]
    ax.plot(xx,sp['coef'][0]*sp['g'],color=GREEN,label=t('Ca II 分量','Ca II component'))
    ax.plot(xx,sp['coef'][1]*sp['h'],color=ORANGE,label=t('模拟干扰峰','Constructed interference'))
    ax.plot(xx,sp['coef'][2]+sp['coef'][3]*sp['x'],color=PURPLE,label=t('拟合背景','Fitted background'))
    ax.set(xlabel=t('空气波长 / nm','Air wavelength / nm'),ylabel=t('信号 / a.u.','Signal / a.u.'),title=t('B  分开核对每一项','B  Inspect each contribution'))
    ax.legend(fontsize=9);ax.ticklabel_format(useOffset=False,axis='x')
    ax=axs[0,1];ax.plot(sp['x'],sp['y']-sp['fit'],color=BLUE,lw=1)
    ax.axhspan(-40,40,color=BLUE,alpha=.08);ax.axhline(0,color='#9eaaaf',lw=1)
    ax.set(xlabel=t('距钙线中心 / nm','Offset from calcium line / nm'),ylabel=t('观测 − 拟合 / a.u.','Observed − fitted / a.u.'),title=t('C  小残差仍需配合可辨识性','C  Small residuals need an identifiability check'))
    sep=np.linspace(.00015,.04,160)
    cond=np.array([spectral_model(separation=s)['condition'] for s in sep])
    ax=axs[1,1];ax.semilogy(sep/.014,cond,color=PURPLE,lw=2)
    ax.axvline(.018/.014,color=ORANGE,ls='--',label=t('当前示例','Current example'))
    ax.set(xlabel=t('峰间距 / 半高全宽','Separation / FWHM'),ylabel=t('投影后条件数 κ','Projected condition number κ'),title=t('D  靠近时噪声被放大','D  Approaching lines amplify noise'));ax.legend(fontsize=9)
    save(fig,'spectral-separation')
    csvsave('spectrum.csv',['air_wavelength_nm','constructed_signal','fitted_signal','residual'],zip(xx,sp['y'],sp['fit'],sp['y']-sp['fit']))

    # 3: calibrations and the complete solid-to-solution calculation.
    rng=np.random.default_rng(805)
    cx=np.repeat([0,.25,.5,1,2],3)
    cy=150+12000*cx+rng.normal(0,30,len(cx))
    slope,intercept=np.polyfit(cx,cy,1)
    uy=150+12000*.8+rng.normal(0,18,3)
    uc=(uy-intercept)/slope
    c=float(uc.mean()); mass=c*10*.05000/.0002500
    residual=cy-(slope*cx+intercept)
    blank=150+12*fixed_noise(10,808)
    sd=float(np.std(blank,ddof=1)); lod=3*sd/slope;loq=10*sd/slope
    fig=plt.figure(figsize=(13,8.6),layout='constrained');gs=fig.add_gridspec(2,2)
    ax=fig.add_subplot(gs[0,0]);ax.scatter(cx,cy,color=BLUE,s=25)
    ax.plot([0,2],[intercept,intercept+2*slope],color=BLUE,lw=1)
    ax.scatter([c],[uy.mean()],color=ORANGE,s=70,zorder=4,label=t('未知液，三次进样均值','Unknown, mean of three injections'))
    ax.set(xlabel=t('标准浓度 / mg L⁻¹','Standard concentration / mg L⁻¹'),ylabel=t('净谱线信号 / a.u.','Net line signal / a.u.'),title=t('A  五个水平，各三次观测','A  Five levels, three observations each'));ax.legend(fontsize=9)
    ax=fig.add_subplot(gs[1,0]);ax.scatter(cx,residual,color=GREEN,s=25);ax.axhline(0,color='#85949c',lw=1)
    ax.set(xlabel=t('标准浓度 / mg L⁻¹','Standard concentration / mg L⁻¹'),ylabel=t('校准残差 / a.u.','Calibration residual / a.u.'),title=t('B  检查弯曲与低端散布','B  Look for curvature and low-end scatter'))
    ax=fig.add_subplot(gs[:,1]);ax.axis('off')
    steps=[t('干基复合材料 0.2500 g','Dry composite specimen: 0.2500 g'),t('完整消解，定容至 50.00 mL','Complete digestion; make to 50.00 mL'),t('消解液再稀释 10 倍','Dilute digest a further tenfold'),t(f'进样液测得 {c:.4f} mg/L',f'Measured solution: {c:.4f} mg/L'),t(f'样品总钙 {mass:.1f} mg/kg',f'Total Ca in specimen: {mass:.1f} mg/kg')]
    for j,label in enumerate(steps):
        y=.88-j*.18;ax.text(.5,y,label,ha='center',va='center',transform=ax.transAxes,fontsize=13,bbox={'boxstyle':'round,pad=.6','fc':'#e9f1f4','ec':'none'})
        if j<4: ax.annotate('',xy=(.5,y-.12),xytext=(.5,y-.05),xycoords='axes fraction',arrowprops={'arrowstyle':'->','color':BLUE})
    ax.set_title(t('C  保存体积与质量，才能回到材料','C  Retain volumes and mass to return to the material'),loc='left')
    save(fig,'calibration-mass')
    csvsave('calibration.csv',['concentration_mg_L','constructed_signal','fitted_signal','residual'],zip(cx,cy,slope*cx+intercept,residual))
    csvsave('unknown.csv',['injection','constructed_signal','concentration_mg_L'],zip(range(1,4),uy,uc))

    # 4: matrix physics and QC. The values here are exact constructed relationships.
    added=np.array([0,.4,.8,1.2]); add_signal=.8*12000*(.8+added)
    add_slope,add_intercept=np.polyfit(added,add_signal,1)
    seq=np.arange(1,17);gain=1-.15*(seq-1)/15
    # Deliberate response mismatch in the last four solutions illustrates limits.
    target_response=gain.copy(); target_response[-4:]*=.92
    fig,axs=plt.subplots(2,2,figsize=(13,8.4),layout='constrained')
    ax=axs[0,0];labels=[t('真实','True'),t('外标','External'),t('内标比值','Internal ratio')]
    ax.bar(labels,[.8,.64,.8],color=[GREEN,ORANGE,BLUE]);ax.set(ylim=(0,1),ylabel=t('浓度 / mg L⁻¹','Concentration / mg L⁻¹'),title=t('A  两条通道共同降为 80%','A  Both channels fall to 80%'))
    ax=axs[0,1];ax.plot(added,add_signal,'o-',color=GREEN);ax.plot([-.8,0],[0,add_intercept],color=GREEN,ls='--');ax.axhline(0,color='#9da7ac',lw=1);ax.axvline(-.8,color=ORANGE,ls=':')
    ax.set(xlabel=t('终体积中加入的钙 / mg L⁻¹','Added calcium in final volume / mg L⁻¹'),ylabel=t('背景扣除信号 / a.u.','Background-corrected signal / a.u.'),title=t('B  标准加入：横截距 −0.800','B  Standard additions: intercept −0.800'))
    ax=axs[1,0];ax.plot(seq,target_response,'o-',color=ORANGE,label=t('外标','External'));ax.plot(seq,target_response/gain,'o-',color=BLUE,label=t('内标校正','Internal correction'));ax.axhline(1,color=GREEN,ls=':')
    ax.axvspan(12.5,16.5,color=PURPLE,alpha=.07);ax.set(xlabel=t('检查液顺序','Check solution sequence'),ylabel=t('测得浓度 / 已知浓度','Measured / known concentration'),ylim=(.7,1.05),title=t('C  最后四份：目标元素额外抑制 8%','C  Last four: extra 8% analyte suppression'));ax.legend(fontsize=9)
    ax=axs[1,1];ax.axis('off');ax.set_title(t('D  校正需要追踪同一种变化','D  Correction must track the same change'),loc='left')
    text=t('共同雾化 / 传输变化\n目标信号 ÷ 内标信号 → 可抵消\n\n额外谱线、消解损失、不同响应\n需要换线、验证制样或改变基体\n\n消解后加标：0.50 mg/L\n外标增量：0.40 mg/L → 回收率 80%',
           'Shared nebulization / transport change\nAnalyte ÷ internal signal → cancels\n\nExtra lines, digestion losses, unequal response\nChange line, validate preparation or matrix\n\nPost-digestion spike: 0.50 mg/L\nExternal increment: 0.40 mg/L → 80% recovery')
    ax.text(.03,.9,text,va='top',linespacing=1.7,fontsize=12,transform=ax.transAxes)
    save(fig,'matrix-quality')
    csvsave('standard_additions.csv',['added_mg_L','constructed_signal'],zip(added,add_signal))
    csvsave('quality_control.csv',['sequence','shared_gain','external_ratio','internal_corrected_ratio'],zip(seq,gain,target_response,target_response/gain))

    # 5: actual NIST certificate values, with element-specific expanded uncertainty.
    with (Path(__file__).parent/'data'/'srm1643f.csv').open(encoding='utf-8') as f:
        cert=list(csv.DictReader(f))
    names=[r['element'] for r in cert]
    values=np.array([float(r['concentration_ug_L'])/1000 for r in cert])
    uncertainty=np.array([float(r['expanded_uncertainty_ug_L'])/1000 for r in cert])
    factors=np.array([float(r['coverage_factor']) for r in cert])
    fig,axs=plt.subplots(1,2,figsize=(13,5.5),layout='constrained');yp=np.arange(4)
    ax=axs[0];ax.errorbar(values,yp,xerr=uncertainty,fmt='o',color=BLUE,capsize=5,ms=7)
    ax.set(xscale='log',yticks=yp,yticklabels=names,xlabel=t('认证质量浓度 / mg L⁻¹（对数轴）','Certified mass concentration / mg L⁻¹ (log scale)'),title=t('A  NIST SRM 1643f 的四个元素','A  Four elements in NIST SRM 1643f'))
    ax.invert_yaxis();ax.grid(axis='x',alpha=.15)
    ax=axs[1];ax.barh(yp,100*uncertainty/values,color=[BLUE,GREEN,PURPLE,ORANGE]);ax.set(yticks=yp,yticklabels=names,xlabel=t('相对扩展不确定度 / %','Relative expanded uncertainty / %'),title=t('B  误差线各有自己的覆盖因子','B  Each interval has its own coverage factor'));ax.invert_yaxis()
    for i,(u,v,k) in enumerate(zip(uncertainty,values,factors)):
        ax.text(100*u/v+.1,i,f'{100*u/v:.2f}%   k={k:.1f}',va='center',fontsize=10)
    ax.set_xlim(0,8.5)
    fig.suptitle(t('证书值与约 95% 扩展不确定度；不是本例的实测重复','Certificate values and ≈95% expanded uncertainty; not replicate measurements in this example'),fontsize=12)
    save(fig,'certified-reference')
    csvsave('certificate_mg_L.csv',['element','concentration_mg_L','expanded_uncertainty_mg_L','k'],zip(names,values,uncertainty,factors))
    summary={'photon_400nm_eV':6.62607015e-34*299792458/(400e-9)/1.602176634e-19,
             'ideal_mass_mg_kg':.8*10*.05000/.0002500,
             'calibration':{'slope':float(slope),'intercept':float(intercept)},
             'unknown_mg_L':c,'sample_Ca_mg_kg':mass,
             'blank_signal_sd':sd,'noise_scale_3s_mg_L':lod,'noise_scale_10s_mg_L':loq,
             'standard_addition_native_mg_L':float(add_intercept/add_slope),
             'post_digest_external_recovery_percent':(.8*1.3-.8*.8)/.5*100,
             'shared_matrix_external_mg_L':.64,'shared_matrix_internal_mg_L':.8,
             'certificate_Ca_mg_L':float(values[0]),'certificate_Sr_relative_U_percent':float(100*uncertainty[2]/values[2]),
             'spectral_default':{k:v for k,v in sp.items() if not isinstance(v,np.ndarray)},
             'model_labels':{'calibration':'constructed','spectra':'constructed','quality_control':'constructed','certificate':'NIST certified facts'}}
    assert abs(summary['ideal_mass_mg_kg']-1600)<1e-9
    assert abs(summary['standard_addition_native_mg_L']-.8)<1e-12
    assert abs(summary['post_digest_external_recovery_percent']-80)<1e-10
    assert spectral_model(separation=0)['identifiable'] is False
    assert .78<c<.82 and 1500<mass<1700
    (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
```

For an actual experiment, replace the known concentrations and observations first, checking whether the recorded signal is a peak height, integrated area or an already processed concentration. Confirm that background and intercept are each handled once, then supply the actual specimen mass, final volume and every dilution step. Use independent checks and suitable recovery evidence to evaluate the result. If two available lines disagree, inspect the spectral windows, background positions, dilution consistency and matrix behaviour. This analysis connects elemental light to the quantities a materials study needs: composition, release and their changes under defined conditions.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/S08.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [EPA SW-846 Method 6010D, Revision 5 (2018)](https://www.epa.gov/sites/default/files/2015-12/documents/6010d.pdf)

   Sample introduction, spectral backgrounds, matrix effects, method blanks and quality control.
2. [EPA Method 200.7, Revision 4.4](https://www.epa.gov/sites/default/files/2015-08/documents/method_200-7_rev_4-4_1994.pdf)

   Operational dissolved/total-recoverable definitions and conditions for standard additions.
3. [Kirchhoff and Bunsen (1860): Chemical Analysis by Observation of Spectra](https://www.chemteam.info/Chem-History/Kirchhoff-Bunsen-1860.html)

   English excerpt of the original discussion of the slit, prism and elemental lines.

   Historical technical reference; no web image or extended quotation reused.
4. [Greenfield, Jones and Berry (1964), Analyst 89, 713–720](https://masspec.scripps.edu/learn/ms/pdf/1964_GreenfieldS.pdf)

   Calcium suppression by phosphorus/aluminium and early high-frequency induction plasma work.

   Historical article hosted by an institutional repository; cited as a technical reference. Chapter diagrams are original.
5. [NIST Handbook: Strong Lines of Calcium](https://physics.nist.gov/PhysRefData/Handbook/Tables/calciumtable2.htm)

   Verify Ca I/Ca II air wavelengths and distinguish line positions from concentration calibration.

   Three factual wavelength entries cited; no database compilation or figure reproduced.
6. [NIST SRM 1643f: Trace Elements in Water, Certificate](https://tsapps.nist.gov/srmext/certificates/1643f.pdf)

   Actual concentrations, expanded uncertainties, coverage factors and concentration versus mass fraction.

   Four non-SRD certificate facts transcribed with attribution under NIST non-SRD data policy; original replot; μg/L converted to mg/L.
7. [EPA: Method Detection Limit Procedure, Revision 2](https://www.epa.gov/sites/default/files/2016-12/documents/mdl-procedure_rev2_12-13-2016.pdf)

   How method detection includes complete preparation and multiple batches of spikes and method blanks.
8. [NIST: Copyright, Fair Use and Licensing Statements](https://www.nist.gov/open/copyright-fair-use-and-licensing-statements-srd-data-software-and-technical-series-publications)

   Attribution, modification notices and terms for non-SRD certificate facts.

   Rights reference; non-SRD terms are not generalized to all SRD databases.
