function tables = get_look_up_tables() 

% Open the file for reading
filename = 'IEA-22-280-RWT_Cp_Ct_Cq.txt';
fid = fopen(filename, 'r');

% Read the file line by line and store non-comment lines
lines = {};
while ~feof(fid)
    lines{end+1} = fgetl(fid);
end


beta_line = strsplit(lines{1}, '   ');
beta_vector = zeros(1, 20); % Preallocate the vector

for i = 1:20
    beta_vector(i) = str2double(beta_line{i}); % Convert to double
end


gamma_line = strsplit(lines{2}, '   ');
gamma_vector = zeros(1, 20); % Preallocate the vector

for i = 1:20
    gamma_vector(i) = str2double(gamma_line{i}); % Convert to double
end

cp_table = zeros(20, 20); % Preallocate the cp table

for i = 4:23 % Start from the 3rd line to the 22nd line
    if i <= length(lines)
        row_data = strsplit(lines{i}, '   '); % Split the line into entries
        row_data(end) = []; % Remove the last element of the row_data
        cp_table(i-3, 1:length(row_data)) = str2double(row_data); % Convert to double and store in the table
    end
end

ct_table = zeros(20, 20); % Preallocate the ct table

for i = 25:44 % Start from the 27th line to the 46th line
    if i <= length(lines)
        row_data = strsplit(lines{i}, '   '); % Split the line into entries
        row_data(end) = []; % Remove the last element of the row_data
        ct_table(i-24, 1:length(row_data)) = str2double(row_data); % Convert to double and store in the table
    end
end

ctau_table = zeros(20, 20); % Preallocate the ctau table

for i = 46:65 % Start from the 47th line to the 66th line
    if i <= length(lines)
        row_data = strsplit(lines{i}, '   '); % Split the line into entries
        row_data(end) = []; % Remove the last element of the row_data
        ctau_table(i-45, 1:length(row_data)) = str2double(row_data); % Convert to double and store in the table
    end
end

% Close the file
fclose(fid);
tables = {cp_table, ct_table, ctau_table, beta_vector, gamma_vector};
end
