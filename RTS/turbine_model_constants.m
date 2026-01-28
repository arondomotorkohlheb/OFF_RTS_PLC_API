xref_lookup = load('xref_lookup.mat');
cp_vector = xref_lookup.cp_vector;
xref_optimal = xref_lookup.solutions;

N = numel(cp_vector);
lambda_array = zeros(1, N);
beta_array = zeros(1, N);
for k = 1:N
    lambda_array(k) = xref_optimal{k}{1};
    beta_array(k) = xref_optimal{k}{2};
end

rho = Simulink.Parameter(1.225);
% todo: find a way to connect the 2 configuration files so 
% only one needs to be changed -> also this file should depend on the 
% config file call within python
Nt = Simulink.Parameter(10);
% beta_opt = Simulink.Parameter(2.895);
R = Simulink.Parameter(142);
A = Simulink.Parameter(R.Value^2*pi);
JT = Simulink.Parameter(2.052*10^8*3);

tables = get_look_up_tables();
cp_table = Simulink.Parameter(tables{1});
ct_table = Simulink.Parameter(tables{2});
ctau_table = Simulink.Parameter(tables{3});
beta_vector = Simulink.Parameter(tables{4});
lambda_vector = Simulink.Parameter(tables{5});
mu = Simulink.Parameter(0.95);

[lambda_max_index, beta_max_index] = find(cp_table.Value == max(cp_table.Value(:)));
lambda_max = lambda_vector.Value(lambda_max_index);
beta_max = beta_vector.Value(beta_max_index);
cp_max = Simulink.Parameter(max(cp_table.Value(:))*0.99);

c_beta_dot = Simulink.Parameter(1);
c_gamma_dot = Simulink.Parameter(1/180*pi);

Ts_inner = Simulink.Parameter(0.1);
Ts_outer = Simulink.Parameter(1);
Ts = Simulink.Parameter(1);

P_omega_dot = Simulink.Parameter(0.5);
P_omega_dot_negative = Simulink.Parameter(0.05);
omega_safety_increase = Simulink.Parameter(1.02);
xref_lookup = load('xref_lookup.mat');

cp_vector = xref_lookup.cp_vector;
xref_optimal = xref_lookup.solutions;

N = numel(cp_vector);
lambda_array = zeros(1, N);
beta_array = zeros(1, N);
for k = 1:N
    lambda_array(k) = xref_optimal{k}{1};
    beta_array(k) = xref_optimal{k}{2};
end
cp_opt_keys = Simulink.Parameter(cell2mat(cp_vector));

lambda_opt_vector = Simulink.Parameter(lambda_array);
beta_opt_vector = Simulink.Parameter(beta_array);

x0 = Simulink.Parameter([0,200/180*pi,0]); % initial states: beta gamma omega for each turbine