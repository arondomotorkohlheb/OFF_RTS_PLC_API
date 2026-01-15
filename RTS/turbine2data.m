% Run the simulation (if not already done)
simOut = sim('turbine_decoupled.slx');

% Access logged signals
logs = simOut.logsout;     % Simulink.SimulationData.Dataset

% Example: access a specific signal by name
power = logs.get('power');

powertime = power.Values.Time;
powerdata = power.Values.Data;

%do the same for beta and omega
beta = logs.get('beta');
omega = logs.get('omega');

betaTime = beta.Values.Time;
betaData = beta.Values.Data;

omegaTime = omega.Values.Time;
omegaData = omega.Values.Data;


%make a matrix of the differnet data and the time and save it as a .mat
%file
time = powertime; % Assuming time is based on the power signal
data = [powerdata, betaData, omegaData]; % Combine power, beta, and omega data
save('turbine_data_slow_conv_decoupled.mat', 'time', 'data'); % Save the time and data matrix to a .mat file
% plot them on 3 subfigures
% for each figure add 10% margin on the max value that it renders on the y
% axis

figure;
subplot(3, 1, 1);
plot(powertime, powerdata);
title('Power vs Time');
xlabel('Time (s)');
ylabel('Power (W)');
subplot(3, 1, 2);
plot(betaTime, betaData);
title('Beta vs Time');
xlabel('Time (s)');
ylabel('Beta (rad)');
subplot(3, 1, 3);
plot(omegaTime, omegaData);
title('Omega vs Time');
xlabel('Time (s)');
ylabel('Omega (rad/s)');
% Display the figure
sgtitle('Turbine Simulation Results'); % Add a super title for the subplots
