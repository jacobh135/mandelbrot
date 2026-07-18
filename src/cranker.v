module cranker (
    input wire clk, rst_n,
    input wire signed [17:0] c_x, c_y,
    output reg cranker_done,
    output reg [4:0] out
);
    reg active;
    reg [4:0] count;
    reg signed [17:0] z_x, z_y, c_x_s, c_y_s;
    wire signed [35:0] z_x_2, z_y_2, z_y_z_x;

    assign z_x_2 = z_x * z_x;
    assign z_y_2 = z_y * z_y;
    assign z_y_z_x = z_x * z_y;

    always @(posedge clk) begin
        if (~rst_n) begin
            out <= 0;
            count <= 0;
            active <= 1;
            z_x <= 0;
            z_y <= 0;
            c_x_s <= c_x;
            c_y_s <= c_y;
            cranker_done <= 0;
        end
        else begin
            case (active)
                1: begin
                    if (count == 24) begin
                        out <= count;
                        count <= 0;
                        z_x <= 0;
                        z_y <= 0;
                        c_x_s <= c_x;
                        c_y_s <= c_y;
                        cranker_done <= 1;
                    end
                    else if (z_x_2 + z_y_2 > 37'sd4294967296) begin
                        out <= count;
                        count <= count + 1;
                        active <= 0;
                        cranker_done <= 0;
                    end
                    else begin
                        z_x <= z_x_2[32:15] - z_y_2[32:15] + c_x_s;
                        z_y <= z_y_z_x[32:15] + z_y_z_x[32:15] + c_y_s;
                        count <= count + 1;
                        cranker_done <= 0;
                    end
                end
                0: begin
                    if (count == 24) begin
                        count <= 0;
                        active <= 1;
                        z_x <= 0;
                        z_y <= 0;
                        c_x_s <= c_x;
                        c_y_s <= c_y;
                        cranker_done <= 1;
                    end
                    else begin
                        count <= count + 1;
                    end
                end
            endcase
        end
    end

endmodule