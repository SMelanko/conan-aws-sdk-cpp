#include <iostream>
#include <aws/core/Aws.h>

int main() {
    Aws::SDKOptions options;
    Aws::InitAPI(options);

    Aws::ShutdownAPI(options);
    return 0;
}

